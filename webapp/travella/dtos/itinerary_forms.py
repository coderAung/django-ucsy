import uuid
from django.http import HttpRequest
from django.core.files.uploadedfile import UploadedFile

from travella.domains.models.tour_models import Itinerary


class ItineraryForm:
    def __init__(self, request:HttpRequest):
        query = request.POST
        self._day:str = query.get('day')
        self._title:str = query.get('title')
        self._description:str = query.get('description')
        self._image:UploadedFile = request.FILES.get('image')
    
    def get_model(self, package_id:uuid) -> Itinerary:
        return Itinerary(
            day = int(self._day),
            title = self._title,
            description = self._description,
            image = self._image,
            package_id = package_id,
        )