from dataclasses import dataclass

from ..domains.models.tour_models import Category, Package

@dataclass
class CategoryItem:
    name:str

    @staticmethod
    def of(category:Category) -> 'CategoryItem':
        return CategoryItem(category.name)

def load_categories() -> list[CategoryItem]:
    return [CategoryItem.of(c) for c in Category.objects.all()]

def load_status() -> dict[Package.Status]:
    return {s.label : s.value for s in Package.Status}.items()

def is_empty(value:str) -> bool:
    if value == None or value == '' or value == 'null':
        return True
    return False