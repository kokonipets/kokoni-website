const nodemailer = require('nodemailer');

module.exports = async (req, res) => {
  // CORS / method guard
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
    const { name = '', phone = '', email = '', subject_line = '', message = '', botcheck = '' } = body;

    // Honeypot spam trap — real users never fill this hidden field
    if (botcheck) {
      return res.status(200).json({ success: true });
    }

    if (!email || !message) {
      return res.status(400).json({ success: false, message: 'Email and message are required.' });
    }

    // Strip CR/LF from any field that ends up in an email header, to prevent header injection
    const stripCrlf = (s) => String(s).replace(/[\r\n]+/g, ' ').trim();
    const safeName = stripCrlf(name);
    const safePhone = stripCrlf(phone);
    const safeSubject = stripCrlf(subject_line);
    const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const safeEmail = emailRe.test(stripCrlf(email)) ? stripCrlf(email) : null;
    if (!safeEmail) {
      return res.status(400).json({ success: false, message: 'A valid email address is required.' });
    }

    const GMAIL_USER = process.env.GMAIL_USER;
    const GMAIL_APP_PASSWORD = process.env.GMAIL_APP_PASSWORD;

    if (!GMAIL_USER || !GMAIL_APP_PASSWORD) {
      console.error('Missing GMAIL_USER or GMAIL_APP_PASSWORD env vars');
      return res.status(500).json({ success: false, message: 'Server email not configured.' });
    }

    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: GMAIL_USER,
        pass: GMAIL_APP_PASSWORD,
      },
    });

    await transporter.sendMail({
      from: `"Kokoni Pet Salon Website" <${GMAIL_USER}>`,
      to: GMAIL_USER,
      replyTo: safeEmail,
      subject: `New Website Message${safeSubject ? ' - ' + safeSubject : ''}`,
      text: `Name: ${safeName}\nPhone: ${safePhone}\nEmail: ${safeEmail}\nSubject: ${safeSubject}\n\nMessage:\n${message}`,
      html: `
        <p><strong>Name:</strong> ${escapeHtml(safeName)}</p>
        <p><strong>Phone:</strong> ${escapeHtml(safePhone)}</p>
        <p><strong>Email:</strong> ${escapeHtml(safeEmail)}</p>
        <p><strong>Subject:</strong> ${escapeHtml(safeSubject)}</p>
        <p><strong>Message:</strong><br/>${escapeHtml(message).replace(/\n/g, '<br/>')}</p>
      `,
    });

    return res.status(200).json({ success: true });
  } catch (err) {
    console.error('Contact form error:', err);
    return res.status(500).json({ success: false, message: 'Something went wrong sending your message.' });
  }
};

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
