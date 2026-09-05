# Proton contact delivery on Render

The existing `alphaworx-io` service (`srv-da0fmo1t0dsc739jvr4g`) is a Static Site
tracking `main`. It serves the approved redesign and calls the separate SMTP
integration through its public configuration URL. The paid Python web service is
`alphaworx-contact`, deployed from `codex/proton-contact`.

- Service ID: `srv-dae6i5ad0e5s73fbkav0`
- URL: https://alphaworx-contact.onrender.com
- Environment: https://dashboard.render.com/web/srv-dae6i5ad0e5s73fbkav0/env
- Compute approved September 5, 2026: $7/month, 0.5 CPU, 512 MB RAM.
- Proton authentication and end-to-end inbox receipt were confirmed on September
  5, 2026. Credentials are stored only in the web service's Render environment.

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
| `PROTON_SMTP_USERNAME` | `info@alphaworx.io` |
| `PROTON_SMTP_TOKEN` | Dedicated Proton SMTP token; secret, never committed |
| `CONTACT_SIGNING_KEY` | A generated random secret of at least 32 bytes |
| `PUBLIC_ORIGIN` | `https://alphaworx.io` |

The app also allows its own `RENDER_EXTERNAL_URL` origin for staging. It exposes
only an enabled flag, a public endpoint, and a short-lived form token to the browser.
Do not put the SMTP token in a Static Site build environment or a JavaScript file.

## Proton token

In Proton Mail: **Settings → All settings → IMAP/SMTP → SMTP tokens → Generate token**.
Name it `Alphaworx website`, select `info@alphaworx.io`, and paste the generated token
directly into the new Render web service's `PROTON_SMTP_TOKEN` environment variable.
Use this dedicated token, never the Proton account password. The server connects
to `smtp.protonmail.ch:587` using certificate-verified STARTTLS.

## Connecting the website

If the site is served by this Python app, the contact form discovers `/api/contact/config`
automatically. If keeping the existing static hosting, set
`ALPHAWORX_CONTACT_CONFIG_URL` in `assets/contact-config.js` to the new service's
`https://alphaworx-contact.onrender.com/api/contact/config` URL. The backend permits CORS
only for the configured public site and its own Render origin. This does not require
a domain or mail DNS change. Publish the revised static homepage separately when ready.

When credentials are missing, the form keeps the existing **Continue in email**
fallback. With credentials, it offers **Send inquiry**. Messages always go to
`info@alphaworx.io`; the visitor's validated email becomes Reply-To. No visitor-supplied
recipient or sender is accepted. Success means Proton accepted the message, not proof
of final inbox placement. Verify receipt in Proton during an authorized live test.

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
- https://proton.me/support/smtp-submission
- https://render.com/docs/free
- https://render.com/docs/deploy-flask
