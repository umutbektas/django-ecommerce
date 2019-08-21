from django.urls import path
from .views import ProductListView, ProductDetailView

app_name = "products"

urlpatterns = [
    path('', ProductListView.as_view(), name="list"),
    path('detail/<slug:slug>/', ProductDetailView.as_view(), name="detail")
]