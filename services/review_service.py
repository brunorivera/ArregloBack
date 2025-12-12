"""Review service with business logic and data operations."""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Dict, Any

from services.base_service_impl import BaseServiceImpl
from models.review import ReviewModel
from schemas.review_schema import ReviewSchema
from repositories.review_repository import ReviewRepository
from repositories.product_repository import ProductRepository


class ReviewService(BaseServiceImpl):
    """Service for Review entity operations."""
    
    def __init__(self, db: Session):
        # Inicializar el servicio base
        super().__init__(
            repository_class=ReviewRepository,
            model=ReviewModel,
            schema=ReviewSchema,
            db=db
        )
        
        # Inicializar repositorio de productos
        self.product_repository = ProductRepository(db)
    
    def create(self, data: Dict[str, Any]) -> ReviewSchema:
        """
        Create a new review.
        
        Args:
            data: Dictionary with review data
            
        Returns:
            ReviewSchema: Created review
        """
        try:
            # Extraer datos
            rating = data.get('rating')
            comment = data.get('comment')
            product_id = data.get('product_id')
            
            # 1. Validaciones básicas
            if rating is None:
                raise ValueError("Rating is required")
            
            if product_id is None:
                raise ValueError("product_id is required")
            
            # 2. Validar rating
            if not isinstance(rating, (int, float)) or rating < 1 or rating > 5:
                raise ValueError("Rating must be a number between 1 and 5")
            
            # 3. Validar product_id
            if not isinstance(product_id, int) or product_id <= 0:
                raise ValueError("product_id must be an integer greater than 0")
            
            # 4. Verificar que el producto existe - ¡CAMBIADO!
            # Usar 'find' en lugar de 'get_by_id'
            product = self.product_repository.find(product_id)
            if not product:
                raise ValueError(f"Product with ID {product_id} does not exist")
            
            # 5. Validar comment
            if comment is not None:
                if not isinstance(comment, str):
                    raise ValueError("Comment must be a string")
                if len(comment) < 10:
                    raise ValueError("Comment must be at least 10 characters if provided")
            
            # 6. Crear ReviewSchema (sin campo 'product')
            review_data = {
                "rating": float(rating),
                "product_id": product_id
            }
            
            # Añadir comment solo si existe
            if comment:
                review_data["comment"] = comment
            
            # 7. Crear schema y guardar
            review_schema = ReviewSchema(**review_data)
            
            # Usar el método save del padre
            return super().save(review_schema)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}"
            )
    
    def save(self, data) -> ReviewSchema:
        """
        Save a review.
        
        Args:
            data: Can be Dict or ReviewSchema
            
        Returns:
            ReviewSchema: Saved review
        """
        if isinstance(data, dict):
            return self.create(data)
        elif isinstance(data, ReviewSchema):
            return self.create(data.model_dump())
        else:
            try:
                return self.create(dict(data))
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot process data: {str(e)}"
                )