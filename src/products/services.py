import logging
from decimal import Decimal
from typing import List
from django.db import transaction
from .models import Product, ProductVariation, ProductImage, Category
from .exceptions import ProductValidationError, ProductNotFoundError, ProductOutOfStockError, ProductImageError
from .schemas import ProductCreateSchema, ProductUpdateSchema, CatalogQuerySchema
from PIL import Image
import os

logger = logging.getLogger(__name__)

def _process_image(file_path: str) -> str:
    """
    Ensures the image is a .png and performs compression.
    """
    if not file_path.lower().endswith('.png'):
        raise ProductImageError("Only .png images are supported.")
    
    img_path = os.path.abspath(file_path)
    try:
        with Image.open(img_path) as img:
            # Ensure it's RGBA/RGB and convert to PNG
            if img.mode != 'RGB' and img.mode != 'RGBA':
                img = img.convert('RGB')
            
            # Add some processing - e.g., slight compression
            img.save(img_path, format='PNG', optimize=True)
        return file_path
    except Exception as e:
        logger.error(f"Error processing image at {file_path}: {e}")
        raise ProductImageError(f"Failed to process image: {e}")

def create_product_listing(schema: ProductCreateSchema) -> Product:
    """
    Handles atomic creation of products, variants, and images.
    """
    try:
        with transaction.atomic():
            category = Category.objects.get(id=schema.category_id)
            
            # Create the product
            product = Product.objects.create(
                title=schema.title,
                description=schema.description,
                base_price=schema.base_price,
                slug=schema.title.lower().replace(' ', '-'), # Simple slug logic
                category=category
            )
            
            # Create variants
            for v_data in schema.variants:
                ProductVariation.objects.create(
                    size_type=v_data.size_type,
                    price_modifier=v_data.price_modifier,
                    product=product
                )
            
            # Handle images
            for i_data in schema.images:
                _process_image(i_data.file_path)
                ProductImage.objects.create(
                    file_path=i_data.file_path,
                    alt_text=i_data.alt_text,
                    is_primary=i_data.is_primary,
                    product=product
                )
            
            return product
    except Category.DoesNotExist:
        raise ProductValidationError("Category does not exist.")
    except Exception as e:
        logger.error(f"Error creating product listing: {e}")
        raise ProductValidationError(str(e))

def get_catalog_data(query: CatalogQuerySchema) -> list:
    """
    Provides optimized data for the front-end.
    """
    query_set = Product.objects.select_related('category').prefetch_related('variations', 'images').all()
    
    if query.category_id:
        query_set = query_set.filter(category_id=query.category_id)
    
    if query.search_term:
        query_set = query_set.filter(title__icontains=query.search_term)
    
    # Basic pagination logic (simulated)
    start = (query.page - 1) * query.page_size
    end = start + query.page_size
    
    return list(query_set[start:end])

def update_stock_level(product_id: int, variation_id: int, quantity_change: int) -> int:
    """
    Manages inventory updates. Note: inventory field would need to exist in model.
    For now, we assume it's part of a concept we're building.
    """
    try:
        variation = ProductVariation.objects.get(id=variation_id, product_id=product_id)
        # In a real scenario, ProductVariation would have a 'stock' or 'quantity' field
        # Since model doesn't have it, we'll simulate a logic check for demonstration
        if quantity_change < 0 and abs(quantity_change) > 100: # Example threshold
             raise ProductOutOfStockError("Requested quantity exceeds available stock.")
        
        # update logic would go here
        return 100 # Updated count (placeholder)
    except ProductVariation.DoesNotExist:
        raise ProductNotFoundError("Variation not found.")
    except Exception as e:
        logger.error(f"Error updating stock: {e}")
        raise ProductValidationError(str(e))
