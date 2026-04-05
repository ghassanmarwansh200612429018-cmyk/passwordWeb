# PassManNNU – Security Architecture Document

## Overview

This document explains the security architecture and protections implemented in PassManNNU, a web-based password manager built with Django.

---

## 1. Data Protection Layers

### 1.1 Vault Password Encryption (AES via Fernet)

- **Algorithm:** Fernet symmetric encryption (AES-128-CBC with HMAC-SHA256)
- **Library:** Python `cryptography` library
- **Implementation:** All vault passwords are encrypted before database storage and decrypted only in-memory during display
- **Key Management:** The encryption key is loaded from the `PASSMANNNU_FERNET_KEY` environment variable — never hardcoded in source code

```
User Input → Fernet.encrypt() → Encrypted blob stored in SQLite
Database → Fernet.decrypt() → Plaintext shown in-memory only
```

### 1.2 Account Password Hashing (PBKDF2)

- **Algorithm:** PBKDF2-SHA256 with 870,000 iterations (Django default)
- **Implementation:** Django's built-in `make_password()` and `check_password()` functions
- **Applies to:** User login passwords and vault passkeys

### 1.3 Passkey Verification

- The passkey is a secondary credential defined during registration
- It is hashed with PBKDF2 (same as account passwords)
- It is required before **editing** or **deleting** any vault entry
- Verification uses Django's `check_password()`, which performs constant-time comparison to prevent timing attacks

---

## 2. Authentication Security

| Protection | Implementation |
|-----------|----------------|
| Session Management | Django sessions with 15-minute timeout (`SESSION_COOKIE_AGE = 900`) |
| Auto-Logout | Custom `AutoLogoutMiddleware` tracks last activity timestamp |
| HttpOnly Cookies | `SESSION_COOKIE_HTTPONLY = True` prevents JavaScript access |
| SameSite Cookies | `SESSION_COOKIE_SAMESITE = 'Lax'` mitigates CSRF via cross-origin |
| Rate Limiting | Session-based counter locks after 5 failed login attempts |

---

## 3. Attack Mitigations

### SQL Injection
- **Mitigation:** Django ORM used exclusively — no raw SQL queries
- All user input passes through Django's parameterized query system

### Cross-Site Scripting (XSS)
- **Mitigation:** Django template engine auto-escapes all variables by default
- No use of `|safe` filter on user-supplied data

### Cross-Site Request Forgery (CSRF)
- **Mitigation:** `CsrfViewMiddleware` enabled globally
- All forms include `{% csrf_token %}`

### Brute-Force Login Attacks
- **Mitigation:** Session-based attempt counter
- Account locks after 5 consecutive failed attempts

### Session Hijacking
- **Mitigation:** `SESSION_EXPIRE_AT_BROWSER_CLOSE = True`
- `SESSION_SAVE_EVERY_REQUEST = True` refreshes the session on each request
- HttpOnly and SameSite cookie flags

---

## 4. Data Flow Summary

```
Registration:
  Password → PBKDF2 hash → auth_user table
  Passkey  → PBKDF2 hash → accounts_userprofile table

Adding Vault Entry:
  Password → Fernet.encrypt() → vault_vaultentry.encrypted_password

Viewing Vault Entry:
  encrypted_password → Fernet.decrypt() → displayed in-memory (never stored in session)

Editing/Deleting:
  User submits passkey → check_password(input, stored_hash) → allow/deny
```

---

## 5. Key Storage Recommendations

For production deployment:
1. Generate a fresh Fernet key: `Fernet.generate_key()`
2. Store it as an environment variable: `PASSMANNNU_FERNET_KEY`
3. Never commit the key to version control
4. Rotate keys periodically using Fernet's `MultiFernet` for backward compatibility

---

*PassManNNU — University Cybersecurity Course Project, 2026*
