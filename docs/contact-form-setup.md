# Contact delivery on Render (Google Workspace SMTP)

The existing `alphaworx-io` service (`srv-da0fmo1t0dsc739jvr4g`) is a Static Site
tracking `main`. It serves the approved redesign and calls the separate SMTP
integration through its public configuration URL. The paid Python web service is
`alphaworx-contact`, deployed from `main`. The same service handles contact
delivery and Google Calendar scheduling, so the scheduler does not require a
second Render service, database, or domain.

- Service ID: `srv-dae6i5ad0e5s73fbkav0`
- URL: https://alphaworx-contact.onrender.com
- Environment: https://dashboard.render.com/web/srv-dae6i5ad0e5s73fbkav0/env
- Compute approved September 5, 2026: $7/month, 0.5 CPU, 512 MB RAM.
- Mail for alphaworx.io moved from Proton to Google Workspace in November 2026. The
  service sends through `smtp.gmail.com`, signed in as `support@alphaworx.io`, and
  delivers to `info@alphaworx.io`. Delivery was confirmed by a live test on November 23,
  2026. Credentials are stored only in the web service's Render environment.

## Render service

- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 90`
- Health check: `/healthz`
- Instance: Starter or another paid web-service instance (free blocks SMTP).
- Auto-deploy: off while reviewing the redesign.
- `render.yaml` contains the equivalent Blueprint configuration.

Set these in the new service's **Environment** settings:

| Variable | Value |
| --- | --- |
| `SMTP_USERNAME` | The Google Workspace account that owns the app password (`support@alphaworx.io`) |
| `SMTP_APP_PASSWORD` | Google app password for that account; secret, never committed |
| `CONTACT_SIGNING_KEY` | A generated random secret of at least 32 bytes |
| `PUBLIC_ORIGIN` | `https://alphaworx.io` |
| `GOOGLE_CLIENT_ID` | OAuth client ID for the Alphaworx Google account |
| `GOOGLE_CLIENT_SECRET` | OAuth client secret; secret, never committed |
| `GOOGLE_REFRESH_TOKEN` | Offline Calendar OAuth refresh token; secret, never committed |
| `GOOGLE_CALENDAR_ID` | `primary` |

The app also allows its own `RENDER_EXTERNAL_URL` origin for staging. It exposes
only an enabled flag, a public endpoint, and a short-lived form token to the browser.
Do not put the app password in a Static Site build environment or a JavaScript file.

## Google app password

Sign in to Google as the account in `SMTP_USERNAME`. 2-Step Verification must be on.
At https://myaccount.google.com/apppasswords create an app password named
`Alphaworx website` and paste it directly into the web service's `SMTP_APP_PASSWORD`
environment variable. Never use the account password. The server connects to
`smtp.gmail.com:587` using certificate-verified STARTTLS. If `info@alphaworx.io` is an
alias and not its own user, set `SMTP_USERNAME` to the user that owns it.

## Connecting the website

If the site is served by this Python app, the contact form discovers `/api/contact/config`
automatically. If keeping the existing static hosting, set
`ALPHAWORX_CONTACT_CONFIG_URL` in `assets/contact-config.js` to the new service's
`https://alphaworx-contact.onrender.com/api/contact/config` URL. The backend permits CORS
only for the configured public site and its own Render origin. This does not require
a domain or mail DNS change. Publish the revised static homepage separately when ready.

## Scheduling

The branded scheduler lives at `https://alphaworx.io/schedule/`. Its browser code
calls the existing contact service for live availability and booking. The service
uses the Google Calendar FreeBusy and Events APIs with the configured refresh
token. It offers 30-minute weekday appointments from 9:00 a.m. to 5:00 p.m.
America/Chicago, requires four hours of notice, and opens dates 30 days ahead.

A confirmed appointment creates a Google Calendar event, requests a Google Meet
conference, adds the visitor as an attendee, and asks Google to send invitations.
The browser receives no Google credential. Availability and booking requests use
short-lived signed tokens and accept production browser requests only from
`https://alphaworx.io`.

When credentials are missing, the form keeps the existing **Continue in email**
fallback. With credentials, it offers **Send inquiry**. Messages always go to
`info@alphaworx.io`; the visitor's validated email becomes Reply-To. No visitor-supplied
recipient or sender is accepted. Success means Google accepted the message, not proof
of final inbox placement. Verify receipt in the inbox during an authorized live test.

## Verification and limits

Run `.venv/bin/python -m unittest discover -s tests -v` for validation, safe email
construction, TLS use, origin checks, secret isolation, rate limits, and duplicate
submission handling. These tests replace SMTP with mocks and never send mail.
For a local backend preview run `.venv/bin/python app.py` (port 57732). Without
credentials it does not send anything. Set local environment variables explicitly;
the app does not automatically load `.env` files.

Requests are limited to 16 KB and messages to 3,000 characters. A honeypot, signed
one-hour form tokens, server validation, and global caps of 3 inquiries/minute and
20/hour reduce abuse. Rate limits are deliberately independent of untrusted proxy
headers. Consider a managed CAPTCHA if actual abuse appears.

A SQLite ledger stores only random form IDs, keyed payload digests, timestamps, and
delivery state for up to 24 hours; no message text or SMTP token is stored in it.
The default `/tmp` ledger survives process restarts but may reset when Render replaces
the instance or deploys. Keep one instance; use durable shared storage before scaling.
Repeated submissions of the same accepted form are acknowledged without resending.
Uncertain SMTP failures are not automatically retried, to avoid duplicate inquiries.

Official references:
- https://support.google.com/accounts/answer/185833
- https://render.com/docs/free
- https://render.com/docs/deploy-flask
