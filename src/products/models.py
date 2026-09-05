from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.CharField(max_length=255, unique=True, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class ProductVariation(models.Model):
    # 'small', 'medium', 'large'
    size_type = models.CharField(max_length=20)
    price_modifier = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.title} - {self.size_type}"

class ProductImage(models.Model):
    file_path = models.CharField(max_length=512)
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.product.title}"
