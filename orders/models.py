from django.db import models
from django.db.models.signals import pre_save, post_save
from addresses.models import Address
from billing.models import BillingProfile
from carts.models import Cart
from ecommerce.utils import unique_order_code_generator
from decimal import Decimal


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded')
)


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        qs = self.get_queryset()\
            .filter(billing_profile=billing_profile, cart=cart_obj, active=True, status='created')\
            .exclude(status='paid')

        if qs.exists():
            created = False
            obj = qs.first()
        else:
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created = True

        return obj, created


class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.SET_NULL, null=True, blank=True)
    order_code = models.CharField(max_length=120, blank=True)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', null=True, blank=True, on_delete=models.SET_NULL)
    billing_address = models.ForeignKey(Address, related_name='billing_address', null=True, blank=True, on_delete=models.SET_NULL)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=False)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(max_digits=30, decimal_places=4, default=10)
    order_total = models.DecimalField(max_digits=30, decimal_places=4, default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.order_code

    objects = OrderManager()

    def check_done(self):
        if self.billing_profile and self.shipping_address and self.billing_address and self.order_total > 0:
            return True
        return False

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = Decimal(cart_total) + Decimal(shipping_total)
        self.order_total = new_total
        self.save()
        return new_total

    def mark_paid(self):
        if self.check_done():
            self.status = 'paid'
            self.save()
        return self.status


def pre_save_create_order_code(sender, instance, *args, **kwargs):
    if not instance.order_code:
        instance.order_code = unique_order_code_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(pre_save_create_order_code, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


post_save.connect(post_save_order, sender=Order)