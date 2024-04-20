from django.db.models.signals import post_save

from stock.task import send_mail
from .models import Order, CartOrder, Shipment, Order_history
from django.dispatch import receiver

@receiver(post_save, sender= Order)
def create_Cart(sender, instance, created, **kwargs):
    if created:
        CartOrder.objects.create(order = instance, product= instance.Product)
        
@receiver(post_save, sender =Shipment)
def check_quantity(sender, instance ,created, **kwargs):
    print('hiii')
    if created:
        Order_history.objects.create(prev_order = instance.ship_order, order_cart = instance.items)
        if instance.ship_order.Product.quantity<=1:
            send_mail.delay(instance.ship_order.Product.Name)