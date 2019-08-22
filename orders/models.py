from django.db import models
from django.db.models.signals import pre_save, post_save

from carts.models import Cart
from ecommerce.utils import unique_order_code_generator


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded')
)


class Order(models.Model):
    order_code = models.CharField(max_length=120, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=False)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(max_digits=30, decimal_places=4, default=10)
    order_total = models.DecimalField(max_digits=30, decimal_places=4, default=0)

    def __str__(self):
        return self.order_code

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = cart_total + shipping_total
        self.order_total = new_total
        self.save()
        return new_total


def pre_save_create_order_code(sender, instance, *args, **kwargs):
    if not instance.order_code:
        instance.order_code = unique_order_code_generator(instance)
        instance.save()


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