from django.http import JsonResponse
from django.shortcuts import render, redirect
from products.models import Product
from .models import Cart
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from addresses.forms import AddressForm
from addresses.models import Address
from decimal import Decimal


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
        'id': x.id,
        'url': x.get_absolute_url(),
        'title': x.title,
        'price': format(x.price, '.2f')
    } for x in cart_obj.products.all()]
    cart_data = {
        'products': products,
        'subTotal': format(cart_obj.subtotal, '.2f'),
        'total': format(cart_obj.total, '.2f')
    }
    return JsonResponse(cart_data, status=200)


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:

        # get product or return cart page
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            # ajax error response
            if request.is_ajax():
                json_data = {
                    'added': False,
                    'removed': False,
                }
                return JsonResponse(json_data, status=409)

            return redirect("carts:home")

        cart_obj, new_obj = Cart.objects.new_or_get(request)

        if product_obj in cart_obj.products.all():
            # remove product cart
            cart_obj.products.remove(product_obj)
            product_added = False
        else:
            # add product cart
            cart_obj.products.add(product_obj)
            product_added = True

        # cart product count update
        request.session['cart_items'] = cart_obj.products.count()

        if request.is_ajax():
            json_data = {
                'added': product_added,
                'removed': not product_added,
                'cartItemCount': cart_obj.products.count(),
            }
            return JsonResponse(json_data, status=200)

    # no product_id in post request
    return redirect("carts:home")


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)

    if cart_created or cart_obj.products.count() == 0:
        return redirect("carts:home")

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == 'POST':
        "some check that order is done"
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect("carts:success")

    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': LoginForm(),
        'guest_form': GuestForm(),
        'address_form': AddressForm(),
        'address_qs': address_qs,
    }

    return render(request, "carts/checkout.html", context)


def checkout_done_view(request):
    context = {
        "order_code": request.POST.get('order_code')
    }
    return render(request, "carts/checkout-done.html", context)
