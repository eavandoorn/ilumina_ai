from django.db import models
from django.utils.null_letters import get_default

class User(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    is_commission_client = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class Contact(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Contact from {self.user if self.user else 'Anonymous'}"
