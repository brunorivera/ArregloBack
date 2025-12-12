"""Review controller with proper dependency injection."""
from fastapi import Depends
from sqlalchemy.orm import Session

from controllers.base_controller_impl import BaseControllerImpl
from schemas.review_schema import ReviewSchema
from services.review_service import ReviewService
from config.database import get_db


class ReviewController(BaseControllerImpl):
    """Controller for Review entity with CRUD operations."""

    def __init__(self):
        super().__init__(
            schema=ReviewSchema,
            service_factory=lambda db: ReviewService(db),
            tags=["Reviews"]
        )

        # ➜ Agregar nueva ruta sin romper el BaseController
        @self.router.get("/by_product/{product_id}", response_model=list[ReviewSchema])
        def get_reviews_by_product(product_id: int, db: Session = Depends(get_db)):

            service = ReviewService(db)

            # Buscar reviews de ese producto
            reviews = db.query(service.model).filter_by(product_id=product_id).all()

            return [ReviewSchema.model_validate(r) for r in reviews]
