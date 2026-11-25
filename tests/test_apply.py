"""Job applications sent from the role pages on alphaworx.io to the contact service (/api/apply)."""
import io
import json
import tempfile
import zipfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from app import CAREERS_FILE, create_app

ROLE = json.loads(CAREERS_FILE.read_text())['roles'][0]['title']


class ApplyTests(unittest.TestCase):
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
        data = dict(name='Test Applicant', email='applicant@example.org', position=ROLE,
            link='https://www.linkedin.com/in/test-applicant', message='An illustrative test application.',
            token=self.client.get('/api/contact/config').json['token'])
        data.update(changes)
        return data

    def post(self, data, origin='https://alphaworx.io'):
        return self.client.post('/api/apply', json=data, headers={'Origin': origin})

    def test_application_is_delivered_to_the_fixed_inbox(self):
        result = self.post(self.payload(to='attacker@example.org', _subject='Overwrite'))
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.headers['Access-Control-Allow-Origin'], 'https://alphaworx.io')
        message = self.sender.call_args.args[0]
        self.assertEqual(message['To'], 'support@alphaworx.io')
        self.assertEqual(message['From'], 'info@alphaworx.io')
        self.assertEqual(message['Reply-To'], 'applicant@example.org')
        self.assertEqual(message['Subject'], f'Job application: {ROLE}')
        body = message.get_content()
        self.assertIn('https://www.linkedin.com/in/test-applicant', body)
        self.assertIn('An illustrative test application.', body)

    def test_note_is_optional(self):
        self.assertEqual(self.post(self.payload(message='')).status_code, 200)
        self.assertIn('Note:\nNot provided', self.sender.call_args.args[0].get_content())

    def test_only_alphaworx_can_send_applications(self):
        for origin in ('https://caiokb.com', 'https://theaikb.com', 'https://example.org'):
            self.assertEqual(self.post(self.payload(), origin=origin).status_code, 403)
        self.sender.assert_not_called()

    def test_role_must_be_an_open_role(self):
        result = self.post(self.payload(position='Chief Executive Officer'))
        self.assertEqual(result.status_code, 400)
        self.sender.assert_not_called()

    def test_link_must_be_a_web_address(self):
        for link in ('linkedin.com/in/someone', 'javascript:alert(1)', 'https://', 'https://exa mple.org', 'ftp://example.org/cv.pdf'):
            self.assertEqual(self.post(self.payload(link=link)).status_code, 400, link)
        self.sender.assert_not_called()

    def test_name_and_email_are_required(self):
        self.assertEqual(self.post(self.payload(name='')).status_code, 400)
        self.assertEqual(self.post(self.payload(email='not-an-email')).status_code, 400)
        self.assertEqual(self.post(self.payload(email='a@example.org\nBcc: x@example.org')).status_code, 400)
        self.sender.assert_not_called()

    def test_form_session_is_required_and_used_once(self):
        self.assertEqual(self.post(self.payload(token='forged')).status_code, 403)
        data = self.payload()
        self.assertEqual(self.post(data).status_code, 200)
        self.assertEqual(self.post(data).status_code, 200)
        self.assertEqual(self.sender.call_count, 1)
        self.assertEqual(self.post({**data, 'message': 'changed'}).status_code, 409)

    def test_honeypot_is_rejected(self):
        self.assertEqual(self.post(self.payload(_gotcha='filled')).status_code, 400)
        self.sender.assert_not_called()


    # Résumé upload (multipart form data)

    def upload(self, content, filename='resume.pdf', origin='https://alphaworx.io', **changes):
        data = self.payload(**changes)
        data['resume'] = (io.BytesIO(content), filename)
        return self.client.post('/api/apply', data=data, content_type='multipart/form-data', headers={'Origin': origin})

    @staticmethod
    def docx():
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as archive:
            archive.writestr('[Content_Types].xml', '<Types/>')
            archive.writestr('word/document.xml', '<w:document/>')
        return buffer.getvalue()

    def test_pdf_resume_is_attached(self):
        result = self.upload(b'%PDF-1.7\n% test resume\n', link='')
        self.assertEqual(result.status_code, 200, result.json)
        message = self.sender.call_args.args[0]
        attachments = list(message.iter_attachments())
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0].get_content_type(), 'application/pdf')
        self.assertEqual(attachments[0].get_filename(), 'Test Applicant - resume.pdf')
        self.assertIn('Résumé: attached (Test Applicant - resume.pdf)', message.get_body(('plain',)).get_content())
        self.assertIn('Link: Not provided', message.get_body(('plain',)).get_content())

    def test_word_resumes_are_accepted(self):
        self.assertEqual(self.upload(self.docx(), 'cv.docx').status_code, 200)
        self.assertEqual(list(self.sender.call_args.args[0].iter_attachments())[0].get_filename(), 'Test Applicant - resume.docx')
        self.assertEqual(self.upload(b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1' + b'\0' * 512, 'cv.doc').status_code, 200)

    def test_file_type_is_judged_by_content_not_name(self):
        for content, name in ((b'MZ\x90\x00 not a resume', 'resume.pdf'), (b'plain text', 'resume.docx'),
                              (b'PK\x03\x04 broken zip', 'resume.docx')):
            self.assertEqual(self.upload(content, name).status_code, 400, name)
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as archive:
            archive.writestr('xl/workbook.xml', '<workbook/>')
        self.assertEqual(self.upload(buffer.getvalue(), 'resume.docx').status_code, 400)
        self.sender.assert_not_called()

    def test_resume_over_5_mb_is_refused(self):
        result = self.upload(b'%PDF-1.7\n' + b'0' * (5 * 1024 * 1024), link='')
        self.assertEqual(result.status_code, 413)
        self.assertIn('under 5 MB', result.json['error'])
        self.sender.assert_not_called()

    def test_file_or_link_is_required(self):
        self.assertEqual(self.post(self.payload(link='')).status_code, 400)
        self.assertEqual(self.client.post('/api/apply', data=self.payload(link=''), content_type='multipart/form-data',
                                          headers={'Origin': 'https://alphaworx.io'}).status_code, 400)
        self.sender.assert_not_called()

    def test_attachment_name_ignores_the_visitors_file_name(self):
        self.assertEqual(self.upload(b'%PDF-1.4\n', '../../<script>evil.exe.pdf', name='Ann <b>O\'Neil</b>').status_code, 200)
        self.assertEqual(list(self.sender.call_args.args[0].iter_attachments())[0].get_filename(), 'Ann bONeilb - resume.pdf')

    def test_upload_only_from_alphaworx(self):
        self.assertEqual(self.upload(b'%PDF-1.7\n', origin='https://caiokb.com').status_code, 403)
        self.sender.assert_not_called()

    def test_contact_form_keeps_its_16_kb_limit(self):
        token = self.client.get('/api/contact/config').json['token']
        result = self.client.post('/api/contact', json=dict(name='A', email='a@example.org', topic='General conversation',
            message='x' * 20000, token=token), headers={'Origin': 'https://alphaworx.io'})
        self.assertEqual(result.status_code, 413)
        self.assertIn('shorten your message', result.json['error'])

if __name__ == '__main__':
    unittest.main()
