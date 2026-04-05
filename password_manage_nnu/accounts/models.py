from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extends the built-in User model with a hashed passkey.
    The passkey is required for edit/delete operations on vault entries.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    passkey_hash = models.CharField(max_length=256)

    def __str__(self):
        return f"Profile of {self.user.username}"
