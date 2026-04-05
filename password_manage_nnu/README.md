# PassManNNU – Secure Password Manager

A secure, full-stack web application for managing credentials with AES encryption. Built with Django, Tailwind CSS, and the Python cryptography library.

> **University Cybersecurity Course Project** — Supports up to ~20 users.

---

## Features

| Feature | Description |
|---------|-------------|
| 🔐 AES Encryption | Vault passwords encrypted with Fernet (AES-128-CBC) |
| 🔑 Passkey Layer | Secondary passkey required for edit/delete operations |
| 🛡️ PBKDF2 Hashing | Account passwords & passkeys hashed with Django's PBKDF2 |
| 🔄 Password Generator | Cryptographically secure (Python `secrets` module), 12–20 chars |
| 📋 Copy to Clipboard | One-click copy with visual "Copied!" feedback |
| 👁️ Visibility Toggle | Show/hide passwords |
| ⏱️ Auto Logout | Session expires after 15 minutes of inactivity |
| 🚫 Rate Limiting | Login attempts limited to prevent brute-force attacks |
| 🌙 Dark Mode | Full dark/light theme with smooth transitions |
| 📱 Responsive UI | Mobile-first design with Tailwind CSS |

---

## Tech Stack

- **Backend:** Python 3.x, Django 6.x
- **Database:** SQLite
- **Frontend:** Django Templates, Tailwind CSS (CDN), Vanilla JavaScript
- **Security:** cryptography library (Fernet), Django auth (PBKDF2)

---

## Quick Start

```bash
# 1. Install dependencies
pip install django cryptography

# 2. Navigate to project
cd passmannnu

# 3. Run migrations
python manage.py makemigrations accounts vault
python manage.py migrate

# 4. (Optional) Create superuser
python manage.py createsuperuser

# 5. Start development server
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** in your browser.

---

## Project Structure

```
passmannnu/
├── manage.py
├── passmannnu/          # Project config
│   ├── settings.py
│   └── urls.py
├── accounts/            # Auth app (register, login, logout, middleware)
│   ├── models.py        # UserProfile (passkey_hash)
│   ├── views.py         # Auth views with rate limiting
│   ├── forms.py         # RegisterForm, LoginForm, PasskeyVerifyForm
│   ├── middleware.py     # Auto-logout on inactivity
│   └── urls.py
├── vault/               # Vault app (CRUD, encryption)
│   ├── models.py        # VaultEntry
│   ├── views.py         # Dashboard, add/edit/delete, passkey verify
│   ├── encryption.py    # Fernet encrypt/decrypt helpers
│   ├── utils.py         # Password generator (secrets module)
│   └── urls.py
├── templates/           # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── about.html
│   ├── contact.html
│   ├── accounts/
│   │   ├── register.html
│   │   └── login.html
│   └── vault/
│       ├── dashboard.html
│       ├── add_entry.html
│       ├── edit_entry.html
│       ├── delete_entry.html
│       └── verify_passkey.html
└── static/
    ├── css/style.css
    └── js/app.js
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PASSMANNNU_FERNET_KEY` | Fernet encryption key for vault passwords | Dev key (change in production!) |

Generate a new key:
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

---

## License

Academic project — for educational use.
