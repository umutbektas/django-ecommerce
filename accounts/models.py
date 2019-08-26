from django.db import models


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
