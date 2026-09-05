// Public configuration URL only. SMTP credentials live in Render Environment.
// When using a separate contact service, set its HTTPS /api/contact/config URL.
// The backend returns a short-lived form token, never the Proton SMTP token.
window.ALPHAWORX_CONTACT_CONFIG_URL = '/api/contact/config';
