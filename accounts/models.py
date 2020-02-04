from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser
)

class User(AbstractBaseUser):
    email = models.EmailField(
        null=False,
        blank=False,
        max_length=80,
        verbose_name='Email'
    )
    full_name = models.CharField(
        null=True,
        blank=True,
        max_length=80,
        verbose_name='Full Name'
    )
    active = models.BooleanField(
        default=True,
        verbose_name='Is Active'
    )
    staff = models.BooleanField(
        default=False,
        verbose_name='Is Staff'
    )
    admin = models.BooleanField(
        default=False,
        verbose_name='Is Admin'
    )

    USERNAME_FIELD = 'email'    # username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []    # python manage.py createsuperuser

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin



class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
