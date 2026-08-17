from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import products.models as p

# --- Customer & Identity ---

class Customer(models.Model):
    """
    Represents a registered user in the system.
    Note: In a production app, you might inherit from Django's built-in User model,
    but for this specific architecture, we are defining it as requested.
    """
    customer_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        return self.email

class Login(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='login_info')
    password = models.CharField(max_length=128)  # Should be hashed in practice
    last_reset = models.DateTimeField(default=timezone.now)


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# --- Logistics & Location ---
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='shipping_addresses')
    street_1 = models.CharField(max_length=255)
    street_2 = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

class BillingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='billing_addresses')
    street_1 = models.CharField(max_length=255)
    street_2 = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

# --- Cart & Shopping ---
class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    session_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    create_time = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} (Session: {self.session_id})"

class CartItem(models.Model):
    session_id = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='session')
    product_id = models.ForeignKey(p.Product, on_delete=models.CASCADE, related_name='pid_cart')
    size = models.IntegerField()  # 1 = Small, 2 = Medium, 3 = Large
    qty = models.IntegerField()
    price = models.IntegerField()

# --- Order Management ---
class Order(models.Model):
    customer_id = models.IntegerField()
    session_id = models.CharField(max_length=100)
    product_id = models.ForeignKey(p.Product, on_delete=models.CASCADE, related_name='pid_orders')
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    create_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    payment_approval = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - Session {self.session_id}"

# --- Communication ---
class Contact(models.Model):
    session_id = models.CharField(max_length=100)
    message = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Contact from {self.session_id}"