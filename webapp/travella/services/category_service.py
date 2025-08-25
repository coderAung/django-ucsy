from django.db import IntegrityError
from travella.domains.models.tour_models import Category
from ..dtos.category_dtos import CategoryDTO
from django.core.exceptions import ObjectDoesNotExist

class CategoryService:
    @staticmethod
    def add_category(name: str, created_by) -> CategoryDTO:
        try:
            category = Category(name=name, created_by=created_by)
            category.save()
            return CategoryDTO.from_model(category)
        except IntegrityError:
            raise ValueError("Category with this name already exists.")

    @staticmethod
    def update_category(id: int, name: str, updated_by) -> CategoryDTO:
        try:
            category = Category.objects.get(pk=id)
            category.name = name
            category.save()
            return CategoryDTO.from_model(category)
        except IntegrityError:
            raise ValueError("Category with this name already exists.")
        except ObjectDoesNotExist:
            raise ValueError("Category not found")

    @staticmethod
    def delete_category(id: int) -> None:
        try:
            category = Category.objects.get(pk=id)
            category.delete()
        except ObjectDoesNotExist:
            raise ValueError("Category not found")