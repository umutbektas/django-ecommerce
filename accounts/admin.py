from django.contrib import admin
from .models import GuestEmail, User


admin.site.register(GuestEmail)

admin.site.register(User)