from travella.domains.models.tour_models import Itinerary, Package
from travella.dtos.itinerary_forms import ItineraryForm


def save(form:ItineraryForm, package_code:str):
    itinerary = form.get_model(Package.objects.get(code = package_code).id)
    itinerary.save()

def delete_by_id(id:int):
    i = Itinerary.objects.get(id=id)
    i.image.delete()
    i.delete()

def get_by_package_code(code:str) -> list['ItineraryDto']:
    _list = Itinerary.objects.filter(package__code = code).order_by('day')
    return [ItineraryDto(i) for i in _list]

class ItineraryDto:
    id:int
    day:int
    title:int
    description:int
    image:str
    package_code:str

    def __init__(self, i:Itinerary):
        self.id = i.id
        self.day = i.day
        self.title = i.title
        self.description = i.description
        try:
            self.image = i.image.url
        except ValueError as e:
            self.image = ''
        self.package_code = i.package.code