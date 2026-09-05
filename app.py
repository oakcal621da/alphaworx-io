"""Alphaworx website and fixed-recipient Proton contact delivery."""
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import secrets
import smtplib
import sqlite3
import ssl
import time
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from uuid import uuid4

from flask import Flask, abort, jsonify, request, send_from_directory, redirect
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge

ROOT = Path(__file__).resolve().parent
SECURITY_HEADERS = json.loads((ROOT / "security-headers.json").read_text())
TOPICS = {
    'General conversation', 'AI strategy assessment', 'Executive AI advisory',
    'AI for growth', 'AI for efficiency', 'Customer experience',
    'Operational resilience', 'AI governance and operations',
}
EMAIL = re.compile(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+")


def valid_email(value):
    return isinstance(value, str) and len(value) <= 254 and bool(EMAIL.fullmatch(value))


def deliver(message, username, token):
    """No visitor-controlled host, envelope recipient, sender, or SMTP headers."""
    smtp = smtplib.SMTP('smtp.protonmail.ch', 587, timeout=8)
    try:
        smtp.ehlo()
        smtp.starttls(context=ssl.create_default_context())
        smtp.ehlo()
        smtp.login(username, token)
        refused = smtp.send_message(message, from_addr=username, to_addrs=['info@alphaworx.io'])
        if refused:
            raise smtplib.SMTPRecipientsRefused(refused)
    finally:
        # DATA acceptance determines success. A failed QUIT must not trigger a resend.
        smtp.close()


def create_app(overrides=None):
    app = Flask(__name__, static_folder=None)
    app.config.update(
        MAX_CONTENT_LENGTH=16 * 1024,
        SECRET_KEY=os.environ.get('CONTACT_SIGNING_KEY') or secrets.token_hex(32),
        SMTP_USERNAME=os.environ.get('PROTON_SMTP_USERNAME', 'info@alphaworx.io').strip(),
        SMTP_TOKEN=os.environ.get('PROTON_SMTP_TOKEN', ''),
        CONTACT_DB=os.environ.get('CONTACT_DB', '/tmp/alphaworx-contact.sqlite3'),
        PUBLIC_ORIGIN=os.environ.get('PUBLIC_ORIGIN', '').rstrip('/'),
        RENDER_ORIGIN=os.environ.get('RENDER_EXTERNAL_URL', '').rstrip('/'),
        MAIL_SENDER=deliver,
    )
    if overrides:
        app.config.update(overrides)
    signer = URLSafeTimedSerializer(app.config['SECRET_KEY'], salt='alphaworx-contact')
    db_path = Path(app.config['CONTACT_DB'])
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as db:
        db.execute('CREATE TABLE IF NOT EXISTS inquiries (id TEXT PRIMARY KEY, digest TEXT NOT NULL, created REAL NOT NULL, state TEXT NOT NULL)')

    def ready():
        return valid_email(app.config['SMTP_USERNAME']) and bool(app.config['SMTP_TOKEN'])

    def allowed_origin():
        configured = {app.config['PUBLIC_ORIGIN'], app.config['RENDER_ORIGIN']} - {''}
        if not configured:
            configured = {'http://127.0.0.1:57732', 'http://localhost:57732'}
        return request.headers.get('Origin') in configured

    def fail(message, code):
        return jsonify(ok=False, error=message), code

    @app.after_request
    def headers(response):
        response.headers.update(SECURITY_HEADERS)
        if request.host.startswith(('127.0.0.1', 'localhost')):
            response.headers.pop('Strict-Transport-Security', None)
            response.headers['Content-Security-Policy'] = SECURITY_HEADERS['Content-Security-Policy'].replace('; upgrade-insecure-requests', '')
        if request.path.startswith('/api/'):
            response.headers['Cache-Control'] = 'no-store'
            if allowed_origin():
                response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
                response.vary.add('Origin')
        elif request.path.endswith(('.html', '.js', '.css')) or request.path == '/':
            response.headers['Cache-Control'] = 'no-cache'
        return response

    @app.errorhandler(RequestEntityTooLarge)
    def too_large(_error):
        return fail('Please shorten your message and try again.', 413)

    @app.get('/healthz')
    def health():
        return jsonify(ok=True)

    @app.get('/api/contact/config')
    def contact_config():
        # A public configuration response contains no SMTP information or credentials.
        if not ready():
            return jsonify(enabled=False)
        return jsonify(enabled=True, endpoint='/api/contact', token=signer.dumps(str(uuid4())))

    @app.post('/api/contact')
    def contact():
        if not allowed_origin():
            return fail('Please submit your inquiry from the Alphaworx website.', 403)
        if not ready():
            return fail('Direct sending is not available yet. Please email info@alphaworx.io.', 503)
        if not request.is_json:
            return fail('Invalid submission format.', 415)
        try:
            data = request.get_json()
        except BadRequest:
            return fail('Invalid submission format.', 400)
        if not isinstance(data, dict):
            return fail('Invalid submission format.', 400)
        if data.get('_gotcha'):
            return fail('Unable to accept this submission.', 400)
        token = data.get('token', '')
        if not isinstance(token, str) or len(token) > 512:
            return fail('Invalid form session. Please reopen the form.', 403)
        try:
            ticket = signer.loads(token, max_age=3600)
        except (BadSignature, SignatureExpired, TypeError):
            return fail('Your form session has expired. Close and reopen the form, then try again.', 403)
        if not isinstance(ticket, str) or len(ticket) != 36:
            return fail('Invalid form session.', 403)
        fields = {}
        for name, limit in [('name', 120), ('email', 254), ('company', 160), ('role', 120), ('topic', 100), ('message', 3000)]:
            value = data.get(name, '')
            if not isinstance(value, str) or len(value) > limit:
                return fail('Please check the length and format of your form fields.', 400)
            value = value.strip()
            if '\x00' in value or (name != 'message' and ('\r' in value or '\n' in value)):
                return fail('Please remove line breaks from the contact details.', 400)
            fields[name] = value
        if not fields['name'] or not fields['message'] or not valid_email(fields['email']):
            return fail('Enter your name, a valid email address, and a message.', 400)
        if fields['topic'] not in TOPICS:
            return fail('Please select one of the conversation topics.', 400)
        digest = hmac.new(app.config['SECRET_KEY'].encode(), json.dumps(fields, sort_keys=True).encode(), hashlib.sha256).hexdigest()
        now = time.time()
        with sqlite3.connect(db_path, timeout=10) as db:
            db.execute('BEGIN IMMEDIATE')
            db.execute('DELETE FROM inquiries WHERE created < ?', (now - 86400,))
            previous = db.execute('SELECT digest, state FROM inquiries WHERE id=?', (ticket,)).fetchone()
            if previous:
                if previous[0] != digest:
                    return fail('Close and reopen the form to start a new inquiry.', 409)
                if previous[1] == 'sent':
                    return jsonify(ok=True)
                if previous[1] == 'sending':
                    return fail('Your inquiry is still being processed. Please wait before trying again.', 409)
                return fail('We could not confirm delivery. Please email info@alphaworx.io before submitting again.', 409)
            # Global limits remain effective even when clients forge proxy headers or
            # obtain multiple form tokens. This app is a small contact form, not a relay.
            minute = db.execute('SELECT count(*) FROM inquiries WHERE created > ?', (now - 60,)).fetchone()[0]
            hour = db.execute('SELECT count(*) FROM inquiries WHERE created > ?', (now - 3600,)).fetchone()[0]
            if minute >= 3 or hour >= 20:
                response = jsonify(ok=False, error='We’re receiving a number of inquiries. Please try again later or email info@alphaworx.io.')
                response.headers['Retry-After'] = '3600' if hour >= 20 else '60'
                return response, 429
            db.execute('INSERT INTO inquiries VALUES (?, ?, ?, ?)', (ticket, digest, now, 'sending'))
        message = EmailMessage()
        message['From'] = app.config['SMTP_USERNAME']
        message['To'] = 'info@alphaworx.io'
        message['Reply-To'] = fields['email']
        message['Subject'] = 'Alphaworx website inquiry: ' + fields['topic']
        message['Date'] = formatdate(localtime=False)
        message['Message-ID'] = make_msgid(domain=app.config['SMTP_USERNAME'].split('@')[1])
        message.set_content(
            'New inquiry from the Alphaworx website\n\n'
            f"Name: {fields['name']}\nEmail: {fields['email']}\n"
            f"Company: {fields['company'] or 'Not provided'}\nRole: {fields['role'] or 'Not provided'}\n"
            f"Topic: {fields['topic']}\n\nMessage:\n{fields['message']}\n"
        )
        try:
            app.config['MAIL_SENDER'](message, app.config['SMTP_USERNAME'], app.config['SMTP_TOKEN'])
        except (smtplib.SMTPException, OSError):
            with sqlite3.connect(db_path) as db:
                db.execute('UPDATE inquiries SET state=? WHERE id=?', ('unconfirmed', ticket))
            # Never log the SMTP exception: it can contain recipient information.
            app.logger.warning('Contact delivery was not confirmed')
            return fail('We couldn’t confirm delivery. Please email info@alphaworx.io directly. Your details are still in the form.', 502)
        with sqlite3.connect(db_path) as db:
            db.execute('UPDATE inquiries SET state=? WHERE id=?', ('sent', ticket))
        return jsonify(ok=True)

    @app.get('/')
    def homepage():
        return send_from_directory(ROOT, 'index.html')

    @app.get('/blog')
    def blog_redirect():
        return redirect('/blog/', code=301)

    @app.get('/blog/')
    def blog_index():
        return send_from_directory(ROOT / 'blog', 'index.html')

    @app.get('/privacy')
    def privacy_redirect():
        return redirect('/privacy/', code=301)

    @app.get('/privacy/')
    def privacy():
        return send_from_directory(ROOT / 'privacy', 'index.html')

    @app.errorhandler(404)
    def missing_page(_error):
        if request.path.startswith('/api/'):
            return fail('Not found.', 404)
        return send_from_directory(ROOT, '404.html'), 404

    @app.get('/<path:filename>')
    def public_file(filename):
        # Serve published content only, never the repository, backend or env files.
        path = Path(filename)
        if filename not in {'index.html', 'deck.html', '404.html', 'robots.txt', 'sitemap.xml'}:
            if not path.parts or path.parts[0] not in {'assets', 'blog'}:
                abort(404)
            if any(part.startswith('.') or part == '..' for part in path.parts):
                abort(404)
            if path.suffix.lower() not in {'.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.svg', '.webp', '.ico', '.woff', '.woff2', '.avif'}:
                abort(404)
        resolved = (ROOT / path).resolve()
        if ROOT not in resolved.parents or not resolved.is_file():
            abort(404)
        return send_from_directory(ROOT, filename)

    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=int(os.environ.get('PORT', '57732')), debug=False)
