from dataclasses import dataclass

from ..domains.models.tour_models import Category


@dataclass
class CategoryItem:
    name:str

    @staticmethod
    def of(category:Category) -> 'CategoryItem':
        return CategoryItem(category.name)

def load_categories() -> list[CategoryItem]:
    return [CategoryItem.of(c) for c in Category.objects.all()]