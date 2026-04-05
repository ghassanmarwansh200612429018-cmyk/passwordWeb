"""
Encryption utilities using Fernet (AES-128-CBC via cryptography library).
All vault passwords are encrypted/decrypted through these helpers.
The Fernet key is loaded from settings (sourced from environment variable).
"""

from django.conf import settings


def encrypt_password(plain_text: str) -> str:
    """Encrypt a plain-text password and return the ciphertext as a UTF-8 string."""
    return settings.FERNET.encrypt(plain_text.encode()).decode()


def decrypt_password(cipher_text: str) -> str:
    """Decrypt a Fernet ciphertext string and return the plain-text password."""
    return settings.FERNET.decrypt(cipher_text.encode()).decode()
