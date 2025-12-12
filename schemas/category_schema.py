"""Category schema with validation."""
from typing import Optional, List, TYPE_CHECKING
from pydantic import Field, ConfigDict
from schemas.base_schema import BaseSchema

if TYPE_CHECKING:
    from schemas.product_schema import ProductSchema

class CategorySchema(BaseSchema):
    """Schema for Category entity with validations."""

    name: str = Field(..., min_length=1, max_length=100, description="Category name (required, unique)")
    
    # COMENTA O ELIMINA ESTA LÍNEA:
    # products: Optional[List['ProductSchema']] = []
    
    # AÑADE ESTA CONFIGURACIÓN:
    model_config = ConfigDict(
        from_attributes=True,
        exclude={"products"}  # ← Esto evita la recursión
    )