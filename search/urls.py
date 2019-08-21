from django.urls import path
from .views import SearchProductListView

app_name = "search"

urlpatterns = [
    path('', SearchProductListView.as_view(), name="products"),
]