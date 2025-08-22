from dataclasses import dataclass
import datetime
import decimal

from travella.domains.models.tour_models import Package, Photo
from travella.utils.constants import BOOK_BEFORE


@dataclass
class PackageCard:
    code:str
    duration:int
    price:decimal
    title:str
    location:str
    cover_photo:str
    category:str
    transportation:Package.Transportation

    def price_display(self) -> str:
        return f'{self.price} MMK / person'

    def days(self) -> str:
        return f'{self.duration} - days'
    
    @staticmethod
    def projections() -> list[str]:
        return ['code', 'duration', 'price', 'title', 'location', 'cover_photo']
    
    def by_transportation(self) -> str:
        return self.transportation.label

    @staticmethod
    def of(p:Package) -> 'PackageCard':
        p.check_status()
        return PackageCard(
            code=p.code,
            duration=p.duration,
            price=p.price,
            title=p.title,
            location=p.location.name if not p.location == None else 'Not Defined',
            cover_photo=p.photos.first().path.url if p.photos.exists() else '',
            category=p.category.name,
            transportation=Package.Transportation(p.transportation)
        )

@dataclass
class PackageDetail(PackageCard):
    tickets:int
    overview:str
    departure:datetime
    photos:list[str]
    status:str

    def departure_to(self) -> datetime:
        return self.departure + datetime.timedelta(self.duration)

    def end_in(self):
        return self.departure - datetime.timedelta(BOOK_BEFORE)

    def remaining_photos(self) -> int:
        return len(self.photos) - 4

    def __init__(self, p:Package):
        self.code = p.code
        self.title = p.title
        self.duration = p.duration
        self.price = p.price
        self.cover_photo = p.photos.first().path.url if p.photos.exists() else ''
        self.location = p.location.name if p.location != None else ''
        self.category = p.category.name
        self.transportation = Package.Transportation(p.transportation)

        self.tickets = p.availableTicket
        self.overview = p.overview
        self.departure = p.departure
        self.photos = [photo.path.url for photo in p.photos.all()]
        self.status = p.status.label
    
    @staticmethod
    def of(p:Package) -> 'PackageDetail':
        return PackageDetail(p)
    