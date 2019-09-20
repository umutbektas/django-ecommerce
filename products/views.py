from django.views.generic import ListView, DetailView
from .models import Product
from carts.models import Cart


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/list.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data()
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    template_name = "products/detail.html"
