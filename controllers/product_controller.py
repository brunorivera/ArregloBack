"""Product controller with proper dependency injection."""
from controllers.base_controller_impl import BaseControllerImpl
from schemas.product_schema import ProductSchema, ProductCreateSchema
from services.product_service import ProductService


class ProductController(BaseControllerImpl):
    """Controller for Product entity with CRUD operations."""

    def __init__(self):
        # Here we tell the base controller to use our new, simpler schema for creation.
        super().__init__(
            schema=ProductSchema,
            create_schema=ProductCreateSchema,
            service_factory=lambda db: ProductService(db),
            tags=["Products"]
        )