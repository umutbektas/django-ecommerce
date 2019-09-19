from django.urls import path
from .views import checkout_address_create_view
app_name = "addresses"

urlpatterns = [
    path('checkout-create-view', checkout_address_create_view, name="checkout_create_view"),
]