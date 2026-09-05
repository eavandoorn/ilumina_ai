from typing import Any
from django.db import models

class ProductError(Exception):
    """Base exception for product errors."""
    pass

class ProductNotFoundError(ProductError):
    """Raised when a product is not found."""
    pass

class ProductValidationError(ProductError):
    """Raised when product validation fails."""
    pass

class ProductImageError(ProductError):
    """Raised when there is an issue with processing or storing product images."""
    pass

class ProductOutOfStockError(ProductError):
    """Raised when a product is out of stock."""
    pass
