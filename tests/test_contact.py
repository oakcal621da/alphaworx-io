import smtplib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from app import create_app, deliver


class ContactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.sender = MagicMock()
        self.app = create_app({'TESTING': True, 'CONTACT_DB': str(Path(self.temp.name) / 'test.db'),
            'SECRET_KEY': 'unit-test-key', 'SMTP_TOKEN': 'fake-test-token',
            'SMTP_USERNAME': 'info@alphaworx.io', 'PUBLIC_ORIGIN': 'https://alphaworx.io',
            'RENDER_ORIGIN': '', 'MAIL_SENDER': self.sender})
        self.client = self.app.test_client()

    def payload(self, **changes):
        data = dict(name='Test Visitor', email='visitor@example.org', company='Meridian Industrial Group',
            role='Operations', topic='AI strategy assessment', message='An illustrative test inquiry.',
            token=self.client.get('/api/contact/config').json['token'])
        data.update(changes)
        return data

    def post(self, data, origin='https://alphaworx.io'):
        return self.client.post('/api/contact', json=data, headers={'Origin': origin})

    def test_fixed_recipient_and_reply_to(self):
        result = self.post(self.payload(to='attacker@example.org', _subject='Overwrite'))
        self.assertEqual(result.status_code, 200)
        message = self.sender.call_args.args[0]
        self.assertEqual(message['To'], 'info@alphaworx.io')
        self.assertEqual(message['From'], 'info@alphaworx.io')
        self.assertEqual(message['Reply-To'], 'visitor@example.org')
        self.assertEqual(message['Subject'], 'Alphaworx website inquiry: AI strategy assessment')
        self.assertIn('Meridian Industrial Group', message.get_content())

    def test_retry_is_not_sent_twice(self):
        data = self.payload()
        self.assertEqual(self.post(data).status_code, 200)
        self.assertEqual(self.post(data).status_code, 200)
        self.sender.assert_called_once()
        self.assertEqual(self.post(dict(data, message='Different inquiry')).status_code, 409)

    def test_failure_does_not_claim_success_or_automatically_resend(self):
        self.sender.side_effect = smtplib.SMTPServerDisconnected('Test failure')
        data = self.payload()
        self.assertEqual(self.post(data).status_code, 502)
        self.assertEqual(self.post(data).status_code, 409)
        self.sender.assert_called_once()

    def test_validation_rejects_malformed_and_injected_fields(self):
        for changes in [dict(name=' '), dict(email='bad'), dict(email='a@b.org\r\nBcc: x@y.org'),
                        dict(role='role\nheader'), dict(message=''), dict(message='x'*3001),
                        dict(name=['wrong type']), dict(topic='Unapproved'), dict(_gotcha='bot')]:
            with self.subTest(changes=changes):
                self.assertEqual(self.post(self.payload(**changes)).status_code, 400)
        self.sender.assert_not_called()

    def test_origin_token_and_media_type(self):
        self.assertEqual(self.post(self.payload(), 'https://elsewhere.example').status_code, 403)
        self.assertEqual(self.post(self.payload(token='bad')).status_code, 403)
        for token in [None, [], {}, 42, 'x' * 513]:
            self.assertEqual(self.post(self.payload(token=token)).status_code, 403)
        self.assertEqual(self.client.post('/api/contact', data='{}', headers={'Origin': 'https://alphaworx.io'}).status_code, 415)
        self.sender.assert_not_called()

    def test_expired_token(self):
        data = self.payload()
        with patch('itsdangerous.timed.TimestampSigner.get_timestamp', return_value=99999999999):
            self.assertEqual(self.post(data).status_code, 403)
        self.sender.assert_not_called()

    def test_spoofed_proxy_headers_do_not_bypass_limits(self):
        for i in range(3):
            self.assertEqual(self.post(self.payload()).status_code, 200)
        result = self.client.post('/api/contact', json=self.payload(), headers={
            'Origin': 'https://alphaworx.io', 'X-Forwarded-For': '203.0.113.99'})
        self.assertEqual(result.status_code, 429)
        self.assertIn('Retry-After', result.headers)
        self.assertEqual(self.sender.call_count, 3)

    def test_configuration_has_no_credentials(self):
        response = self.client.get('/api/contact/config')
        self.assertEqual(set(response.json), {'enabled', 'endpoint', 'token'})
        self.assertNotIn('fake-test-token', response.text)
        self.assertEqual(response.headers['Cache-Control'], 'no-store')
        self.app.config['SMTP_TOKEN'] = ''
        self.assertEqual(self.client.get('/api/contact/config').json, {'enabled': False})
        self.assertEqual(self.post({}).status_code, 503)

    def test_static_allowlist_and_size_limit(self):
        for path in ['/.env', '/.git/config', '/app.py', '/requirements.txt', '/docs/contact-form-setup.md', '/assets/../app.py']:
            self.assertEqual(self.client.get(path).status_code, 404, path)
        for path in ['/', '/assets/contact.js', '/blog/index.html', '/robots.txt']:
            with self.client.get(path) as response:
                self.assertEqual(response.status_code, 200, path)
        result = self.client.post('/api/contact', data='x'*17000, content_type='application/json', headers={'Origin': 'https://alphaworx.io'})
        self.assertEqual(result.status_code, 413)

    def test_cors_only_for_expected_site(self):
        response = self.client.options('/api/contact', headers={'Origin': 'https://alphaworx.io'})
        self.assertEqual(response.headers['Access-Control-Allow-Origin'], 'https://alphaworx.io')
        response = self.client.options('/api/contact', headers={'Origin': 'https://elsewhere.example'})
        self.assertNotIn('Access-Control-Allow-Origin', response.headers)

    @patch('app.smtplib.SMTP')
    def test_smtp_tls_authentication_and_envelope(self, smtp_class):
        smtp = smtp_class.return_value
        smtp.send_message.return_value = {}
        message = MagicMock()
        deliver(message, 'info@alphaworx.io', 'fake-token')
        smtp_class.assert_called_once_with('smtp.protonmail.ch', 587, timeout=8)
        self.assertTrue(smtp.starttls.called)
        smtp.login.assert_called_once_with('info@alphaworx.io', 'fake-token')
        smtp.send_message.assert_called_once_with(message, from_addr='info@alphaworx.io', to_addrs=['info@alphaworx.io'])
        smtp.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
