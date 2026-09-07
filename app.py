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
import threading
import time
from datetime import date, datetime, time as datetime_time, timedelta, timezone
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
from uuid import uuid4
from zoneinfo import ZoneInfo

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
SCHEDULE_TIME_ZONE = ZoneInfo('America/Chicago')
SCHEDULE_START_HOUR = 9
SCHEDULE_END_HOUR = 17
SCHEDULE_DURATION_MINUTES = 30
SCHEDULE_MINIMUM_NOTICE = timedelta(hours=4)
SCHEDULE_WINDOW_DAYS = 30


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


class GoogleCalendar:
    """Minimal single-calendar client for the Alphaworx booking page."""
    def __init__(self, client_id, client_secret, refresh_token, calendar_id='primary'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.calendar_id = calendar_id or 'primary'
        self._access_token = ''
        self._expires_at = 0
        self._lock = threading.Lock()

    def _json_request(self, url, method='GET', payload=None, access_token=None):
        data = None if payload is None else json.dumps(payload).encode()
        headers = {'Accept': 'application/json'}
        if data is not None:
            headers['Content-Type'] = 'application/json'
        if access_token:
            headers['Authorization'] = f'Bearer {access_token}'
        response = urlopen(Request(url, data=data, headers=headers, method=method), timeout=10)
        return json.loads(response.read().decode())

    def _token(self):
        with self._lock:
            if self._access_token and self._expires_at > time.time() + 60:
                return self._access_token
            body = urlencode({
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'refresh_token': self.refresh_token,
                'grant_type': 'refresh_token',
            }).encode()
            response = urlopen(Request('https://oauth2.googleapis.com/token', data=body,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}, method='POST'), timeout=10)
            result = json.loads(response.read().decode())
            token = result.get('access_token')
            if not isinstance(token, str) or not token:
                raise RuntimeError('Google did not return an access token.')
            self._access_token = token
            self._expires_at = time.time() + int(result.get('expires_in', 3600))
            return token

    def busy(self, starts_at, ends_at):
        result = self._json_request('https://www.googleapis.com/calendar/v3/freeBusy', 'POST', {
            'timeMin': starts_at.isoformat(), 'timeMax': ends_at.isoformat(),
            'timeZone': 'America/Chicago', 'items': [{'id': self.calendar_id}],
        }, self._token())
        return result.get('calendars', {}).get(self.calendar_id, {}).get('busy', [])

    def create(self, event_id, starts_at, ends_at, visitor):
        path = quote(self.calendar_id, safe='')
        result = self._json_request(
            f'https://www.googleapis.com/calendar/v3/calendars/{path}/events?conferenceDataVersion=1&sendUpdates=all',
            'POST', {
                'id': event_id,
                'summary': 'Alphaworx — Enterprise AI Strategy Conversation',
                'description': (
                    f"Visitor: {visitor['name']} <{visitor['email']}>\n"
                    f"Company: {visitor['company'] or 'Not provided'}\n\n"
                    f"Conversation context:\n{visitor['message'] or 'Not provided'}"
                ),
                'start': {'dateTime': starts_at.isoformat(), 'timeZone': 'America/Chicago'},
                'end': {'dateTime': ends_at.isoformat(), 'timeZone': 'America/Chicago'},
                'attendees': [{'email': visitor['email'], 'displayName': visitor['name']}],
                'conferenceData': {'createRequest': {
                    'requestId': str(uuid4()),
                    'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                }},
                'guestsCanInviteOthers': False,
                'guestsCanModify': False,
            }, self._token())
        return {'eventId': result.get('id'), 'meetingUrl': result.get('hangoutLink')}


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
        GOOGLE_CLIENT_ID=os.environ.get('GOOGLE_CLIENT_ID', ''),
        GOOGLE_CLIENT_SECRET=os.environ.get('GOOGLE_CLIENT_SECRET', ''),
        GOOGLE_REFRESH_TOKEN=os.environ.get('GOOGLE_REFRESH_TOKEN', ''),
        GOOGLE_CALENDAR_ID=os.environ.get('GOOGLE_CALENDAR_ID', 'primary'),
        CALENDAR_CLIENT=None,
    )
    if overrides:
        app.config.update(overrides)
    signer = URLSafeTimedSerializer(app.config['SECRET_KEY'], salt='alphaworx-contact')
    schedule_signer = URLSafeTimedSerializer(app.config['SECRET_KEY'], salt='alphaworx-schedule')
    db_path = Path(app.config['CONTACT_DB'])
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as db:
        db.execute('CREATE TABLE IF NOT EXISTS inquiries (id TEXT PRIMARY KEY, digest TEXT NOT NULL, created REAL NOT NULL, state TEXT NOT NULL)')
        db.execute('CREATE TABLE IF NOT EXISTS schedule_bookings (id TEXT PRIMARY KEY, digest TEXT NOT NULL, created REAL NOT NULL, state TEXT NOT NULL, response TEXT)')

    calendar_client = app.config['CALENDAR_CLIENT']
    if calendar_client is None and all((app.config['GOOGLE_CLIENT_ID'], app.config['GOOGLE_CLIENT_SECRET'], app.config['GOOGLE_REFRESH_TOKEN'])):
        calendar_client = GoogleCalendar(app.config['GOOGLE_CLIENT_ID'], app.config['GOOGLE_CLIENT_SECRET'],
            app.config['GOOGLE_REFRESH_TOKEN'], app.config['GOOGLE_CALENDAR_ID'])

    def ready():
        return valid_email(app.config['SMTP_USERNAME']) and bool(app.config['SMTP_TOKEN'])

    def schedule_ready():
        return calendar_client is not None

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
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Schedule-Token'
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

    @app.get('/api/schedule/config')
    def schedule_config():
        if not schedule_ready():
            return jsonify(enabled=False)
        return jsonify(enabled=True, availabilityEndpoint='/api/schedule/availability',
            bookingEndpoint='/api/schedule/book', durationMinutes=SCHEDULE_DURATION_MINUTES,
            timeZone='America/Chicago', token=schedule_signer.dumps(str(uuid4())))

    def schedule_ticket():
        token = request.headers.get('X-Schedule-Token', '')
        if not token and request.is_json:
            payload = request.get_json(silent=True)
            token = payload.get('token', '') if isinstance(payload, dict) else ''
        if not isinstance(token, str) or len(token) > 512:
            return None
        try:
            ticket = schedule_signer.loads(token, max_age=3600)
        except (BadSignature, SignatureExpired, TypeError):
            return None
        return ticket if isinstance(ticket, str) and len(ticket) == 36 else None

    def parse_schedule_date(value):
        try:
            requested = date.fromisoformat(value)
        except (TypeError, ValueError):
            return None
        today = datetime.now(SCHEDULE_TIME_ZONE).date()
        if requested < today or requested > today + timedelta(days=SCHEDULE_WINDOW_DAYS) or requested.weekday() > 4:
            return None
        return requested

    def available_slots(requested):
        day_start = datetime.combine(requested, datetime_time(SCHEDULE_START_HOUR), SCHEDULE_TIME_ZONE)
        day_end = datetime.combine(requested, datetime_time(SCHEDULE_END_HOUR), SCHEDULE_TIME_ZONE)
        busy = calendar_client.busy(day_start, day_end)
        intervals = []
        for item in busy:
            try:
                intervals.append((datetime.fromisoformat(item['start'].replace('Z', '+00:00')),
                    datetime.fromisoformat(item['end'].replace('Z', '+00:00'))))
            except (KeyError, TypeError, ValueError):
                continue
        minimum = datetime.now(timezone.utc) + SCHEDULE_MINIMUM_NOTICE
        slots = []
        current = day_start
        while current + timedelta(minutes=SCHEDULE_DURATION_MINUTES) <= day_end:
            ending = current + timedelta(minutes=SCHEDULE_DURATION_MINUTES)
            if current.astimezone(timezone.utc) >= minimum and not any(current < busy_end and ending > busy_start for busy_start, busy_end in intervals):
                slots.append(current.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z'))
            current = ending
        return slots

    @app.get('/api/schedule/availability')
    def schedule_availability():
        if request.headers.get('Origin') and not allowed_origin():
            return fail('Please use the Alphaworx scheduling page.', 403)
        if not schedule_ready():
            return fail('Online scheduling is temporarily unavailable.', 503)
        if not schedule_ticket():
            return fail('Your scheduling session has expired. Refresh the page and try again.', 403)
        requested = parse_schedule_date(request.args.get('date'))
        if requested is None:
            return fail('Choose an available weekday within the next 30 days.', 400)
        try:
            slots = available_slots(requested)
        except (HTTPError, URLError, OSError, RuntimeError, ValueError):
            app.logger.warning('Calendar availability could not be confirmed')
            return fail('We could not load availability. Please try again shortly.', 502)
        return jsonify(ok=True, date=requested.isoformat(), slots=slots)

    @app.post('/api/schedule/book')
    def schedule_book():
        if not allowed_origin():
            return fail('Please use the Alphaworx scheduling page.', 403)
        if not schedule_ready():
            return fail('Online scheduling is temporarily unavailable.', 503)
        if not request.is_json:
            return fail('Invalid booking format.', 415)
        try:
            data = request.get_json()
        except BadRequest:
            return fail('Invalid booking format.', 400)
        if not isinstance(data, dict) or data.get('_gotcha'):
            return fail('Invalid booking format.', 400)
        ticket = schedule_ticket()
        if ticket is None:
            return fail('Your scheduling session has expired. Refresh the page and try again.', 403)
        visitor = {}
        for name, limit in [('name', 120), ('email', 254), ('company', 160), ('message', 1500)]:
            value = data.get(name, '')
            if not isinstance(value, str) or len(value) > limit or '\x00' in value:
                return fail('Please check your booking details.', 400)
            visitor[name] = value.strip()
        if not visitor['name'] or not valid_email(visitor['email']):
            return fail('Enter your name and a valid email address.', 400)
        try:
            starts_at = datetime.fromisoformat(str(data.get('start', '')).replace('Z', '+00:00')).astimezone(SCHEDULE_TIME_ZONE)
        except (TypeError, ValueError):
            return fail('Choose an available time.', 400)
        if starts_at.second or starts_at.microsecond or starts_at.minute not in (0, 30):
            return fail('Choose an available time.', 400)
        requested = parse_schedule_date(starts_at.date().isoformat())
        if requested is None or starts_at.hour < SCHEDULE_START_HOUR or starts_at.hour >= SCHEDULE_END_HOUR:
            return fail('Choose an available time.', 400)
        canonical_start = starts_at.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')
        digest = hmac.new(app.config['SECRET_KEY'].encode(), json.dumps({'start': canonical_start, **visitor}, sort_keys=True).encode(), hashlib.sha256).hexdigest()
        now = time.time()
        with sqlite3.connect(db_path, timeout=10) as db:
            db.execute('BEGIN IMMEDIATE')
            db.execute('DELETE FROM schedule_bookings WHERE created < ?', (now - 86400,))
            previous = db.execute('SELECT digest, state, response FROM schedule_bookings WHERE id=?', (ticket,)).fetchone()
            if previous:
                if previous[0] != digest:
                    return fail('Refresh the page to start a new booking.', 409)
                if previous[1] == 'sent' and previous[2]:
                    return jsonify(ok=True, **json.loads(previous[2]))
                return fail('This booking is already being processed. Refresh availability before trying again.', 409)
            recent = db.execute('SELECT count(*) FROM schedule_bookings WHERE created > ?', (now - 3600,)).fetchone()[0]
            if recent >= 20:
                response = jsonify(ok=False, error='Online scheduling is busy. Please try again later or send an inquiry.')
                response.headers['Retry-After'] = '3600'
                return response, 429
            db.execute('INSERT INTO schedule_bookings VALUES (?, ?, ?, ?, ?)', (ticket, digest, now, 'sending', None))
        try:
            if canonical_start not in available_slots(requested):
                raise ValueError('unavailable')
            ending = starts_at + timedelta(minutes=SCHEDULE_DURATION_MINUTES)
            event_id = 'a' + hashlib.sha256(canonical_start.encode()).hexdigest()[:31]
            result = calendar_client.create(event_id, starts_at, ending, visitor)
            response_data = {'start': canonical_start, 'durationMinutes': SCHEDULE_DURATION_MINUTES,
                'timeZone': 'America/Chicago', 'meetingUrl': result.get('meetingUrl')}
        except HTTPError as error:
            state = 'unavailable' if error.code == 409 else 'unconfirmed'
            with sqlite3.connect(db_path) as db:
                db.execute('UPDATE schedule_bookings SET state=? WHERE id=?', (state, ticket))
            if error.code == 409:
                return fail('That time was just taken. Refresh availability and choose another.', 409)
            app.logger.warning('Calendar booking could not be confirmed')
            return fail('We could not confirm the booking. Please try again shortly.', 502)
        except ValueError:
            with sqlite3.connect(db_path) as db:
                db.execute('UPDATE schedule_bookings SET state=? WHERE id=?', ('unavailable', ticket))
            return fail('That time is no longer available. Refresh availability and choose another.', 409)
        except (URLError, OSError, RuntimeError):
            with sqlite3.connect(db_path) as db:
                db.execute('UPDATE schedule_bookings SET state=? WHERE id=?', ('unconfirmed', ticket))
            app.logger.warning('Calendar booking could not be confirmed')
            return fail('We could not confirm the booking. Please try again shortly.', 502)
        encoded = json.dumps(response_data)
        with sqlite3.connect(db_path) as db:
            db.execute('UPDATE schedule_bookings SET state=?, response=? WHERE id=?', ('sent', encoded, ticket))
        return jsonify(ok=True, **response_data)

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

    @app.get('/schedule')
    def schedule_redirect():
        return redirect('/schedule/', code=301)

    @app.get('/schedule/')
    def schedule():
        return send_from_directory(ROOT / 'schedule', 'index.html')

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
            if not path.parts or path.parts[0] not in {'assets', 'blog', 'schedule'}:
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
