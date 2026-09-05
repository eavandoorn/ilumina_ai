from django.db import models
from django.db.models.JSONField import JSONField

class Cart(models.Model):
    session_token = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20)
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Cart {self.session_token}"

class CartItem(models.Model):
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    variation = models.ForeignKey('products.ProductVariation', related_name='cart_items', on_delete=models.CASCADE)

    def __str__(self):
        return f"CartItem for {self.variation.product.title} (Qty: {self.quantity})"

class Order(models.Model):
    status = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_tx_id = models.CharField(max_length=255, blank=True, null=True)
    shipment_tracking = models.CharField(max_length=255, blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.id}"

class OrderLogistics(models.Model):
    shipping_address = models.JSONField()
    billing_address = models.JSONField()
    order = models.ForeignKey(Order, related_name='logistics', on_delete=models.CASCADE)

    def __str__(self):
        return f"Logistics for Order {self.order.id}"
