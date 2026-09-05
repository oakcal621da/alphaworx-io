// Public configuration URL only. SMTP credentials live in Render Environment.
// The production static site uses the separate Render contact service.
// The backend returns a short-lived form token, never the Proton SMTP token.
window.ALPHAWORX_CONTACT_CONFIG_URL = 'https://alphaworx-contact.onrender.com/api/contact/config';
