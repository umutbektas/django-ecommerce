from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_page, contact_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name="home_url"),
    path('contact/', contact_page, name="contact_url"),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('addresses/', include('addresses.urls')),
    path('cart/', include('carts.urls')),
    path('search/', include('search.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)