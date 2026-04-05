from django.db import models
from django.contrib.auth.models import User


class VaultEntry(models.Model):
    """
    A single credential record inside a user's vault.
    The password field stores Fernet-encrypted ciphertext only.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vault_entries')
    website_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    encrypted_password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name_plural = 'Vault Entries'

    def __str__(self):
        return f"{self.website_name} ({self.username})"
