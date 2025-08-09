from travella.domains.models.tour_models import Category
from ..dtos.category_dtos import CategoryDTO
from django.core.exceptions import ValidationError

class CategoryService:
    @staticmethod
    def add_category(name: str, created_by) -> CategoryDTO:
        try:
            category = Category(name=name, createdBy=created_by)
            category.save()
            return CategoryDTO.from_model(category)
        except ValidationError as e:
            raise ValueError(f"Error adding category: {e}")

        except Exception as e:
            raise ValueError(f"An error occurred: {e}")
