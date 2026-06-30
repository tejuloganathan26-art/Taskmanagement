from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('member', 'Member'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    mobile = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.username


# ---------------- Profile Model ----------------

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=100)

    department = models.CharField(max_length=100)

    designation = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    address = models.TextField()

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )

    bio = models.TextField(blank=True)

    def __str__(self):
        return self.full_name
    
    