import secrets
import string


def generate_password(length: int = 16) -> str:
    """
    Generate a cryptographically secure random password.
    Uses Python's secrets module (CSPRNG).
    Guarantees at least one char from each category.
    """
    if length < 12:
        length = 12
    if length > 20:
        length = 20

    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    symbols = '!@#$%^&*()-_=+[]{}|;:,.<>?'

    # Ensure at least one of each
    password_chars = [
        secrets.choice(upper),
        secrets.choice(lower),
        secrets.choice(digits),
        secrets.choice(symbols),
    ]

    all_chars = upper + lower + digits + symbols
    password_chars += [secrets.choice(all_chars) for _ in range(length - 4)]

    # Shuffle securely
    result = list(password_chars)
    # Fisher-Yates shuffle using secrets
    for i in range(len(result) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        result[i], result[j] = result[j], result[i]

    return ''.join(result)
