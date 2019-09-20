from django.urls import path
from .views import cart_home, cart_update, checkout_home, checkout_done_view, cart_detail_api_view

app_name = "carts"

urlpatterns = [
    path('', cart_home, name="home"),
    path('api/', cart_detail_api_view, name="home_api"),
    path('checkout/', checkout_home, name="checkout"),
    path('update/', cart_update, name="update"),
    path('success/', checkout_done_view, name="success"),
]