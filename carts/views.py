from django.shortcuts import render, redirect
from products.models import Product
from .models import Cart
from orders.models import Order
from ecommerce.utils import unique_order_code_generator
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect("carts:home")

        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)

        request.session['cart_items'] = cart_obj.products.count()

        if request.POST.get('in_cart'):
            return redirect("carts:home")
        return redirect(product_obj.get_absolute_url())
    return redirect("carts:home")


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("carts:home")
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(
            cart=cart_obj,
            defaults={
                'cart': cart_obj,
                'order_code': unique_order_code_generator(Order())
            }
        )

    user = request.user
    billing_profile = None
    guest_email_id = request.session.get('guest_email_id')
    if user.is_authenticated:
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)

    elif guest_email_id is not None:
        email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(email=email_obj.email)

    else:
        pass

    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': LoginForm(),
        'guest_form': GuestForm(),
    }

    return render(request, "carts/checkout.html", context)
