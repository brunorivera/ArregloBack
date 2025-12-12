"""Product schema for request/response validation."""
from typing import Optional, List, TYPE_CHECKING
from pydantic import Field, BaseModel

from schemas.base_schema import BaseSchema

if TYPE_CHECKING:
    from schemas.category_schema import CategorySchema
    from schemas.order_detail_schema import OrderDetailSchema
    from schemas.review_schema import ReviewSchema


class ProductSchema(BaseSchema):
    """Schema for Product entity with validations (used for responses)."""

    name: str = Field(..., min_length=1, max_length=200, description="Product name (required)")
    price: float = Field(..., gt=0, description="Product price (must be greater than 0, required)")
    stock: int = Field(default=0, ge=0, description="Product stock quantity (must be >= 0)")
    category_id: int = Field(..., description="Category ID reference (required)")

    # The 'category' field below is what caused the original error.
    # It remains here for responses, so you get the full category object back.
    category: Optional['CategorySchema'] = None
   # reviews: Optional[List['ReviewSchema']] = []
    order_details: Optional[List['OrderDetailSchema']] = []


class ProductCreateSchema(BaseModel):
    """Schema for creating a Product (used for requests)."""

    name: str = Field(..., min_length=1, max_length=200, description="Product name (required)")
    price: float = Field(..., gt=0, description="Product price (must be greater than 0, required)")
    stock: int = Field(default=0, ge=0, description="Product stock quantity (must be >= 0)")
    category_id: int = Field(..., description="Category ID reference (required)")