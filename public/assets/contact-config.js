// Public configuration URL only. SMTP credentials live in Render Environment.
// The production static site uses the separate Render contact service.
// The backend returns a short-lived form token, never the Proton SMTP token.
const alphaworxLocalBackend = /^(localhost|127\.0\.0\.1)$/.test(window.location.hostname);
window.ALPHAWORX_CONTACT_CONFIG_URL = alphaworxLocalBackend ? '/api/contact/config' : 'https://alphaworx-contact.onrender.com/api/contact/config';
window.ALPHAWORX_SCHEDULER_API_BASE = alphaworxLocalBackend ? window.location.origin : 'https://alphaworx-contact.onrender.com';
