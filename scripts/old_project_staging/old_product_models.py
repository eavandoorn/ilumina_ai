from django.db import models

# --- Product & Inventory ---

class Product(models.Model):
    product = models.AutoField(primary_key=True)
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=50, default='test') # TODO: Update default to a more sensible value
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    main_image = models.ForeignKey('ProductImage', related_name='main_ref', on_delete=models.SET_NULL, null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Product {self.product}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image_file = models.ImageField(upload_to='products/%Y/%m/%d/') 
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)     

# In a production webshop, you don't want to serve a 5MB high-res photo as a small thumbnail. While Django doesn't do this automatically, your model structure should support it.

# Best Practice: Don't try to handle resizing in the models.py. Instead:

# Upload the original image via the ProductImage model.
# Use a library like django-imagekit or sorl-thumbnail. These libraries allow you to define "processed" versions of images that are generated on demand and cached.

