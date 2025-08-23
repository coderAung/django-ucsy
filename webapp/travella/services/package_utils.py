from dataclasses import dataclass
from django.db.models import Sum
from ..domains.models.tour_models import Category, Location, Package
from ..domains.models.booking_models import Booking

@dataclass
class CategoryItem:
    id:int
    name:str

    @staticmethod
    def of(category:Category) -> 'CategoryItem':
        return CategoryItem(category.id, category.name)

def load_categories() -> list[CategoryItem]:
    return [CategoryItem.of(c) for c in Category.objects.all()]

def load_status() -> dict[Package.Status]:
    return {s.label : s.value for s in Package.Status}.items()

def is_empty(value:str) -> bool:
    if value == None or value == '' or value == 'null':
        return True
    return False

@dataclass
class LocationItem:
    id:int
    name:str

    @staticmethod
    def of(l:Location) -> 'LocationItem':
        return LocationItem(l.id, l.name)

def load_locations():
    return [LocationItem.of(l) for l in Location.objects.all()]

# NEW FUNCTIONS FOR AVAILABLE TICKETS CALCULATION
