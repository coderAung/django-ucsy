from dataclasses import dataclass
import decimal

from travella.domains.models.tour_models import Package, Photo


@dataclass
class PackageCard:
    code:str
    duration:int
    price:decimal
    title:str
    location:str
    cover_photo:str
    category:str

    def price_display(self) -> str:
        return f'{self.price} MMK / person'

    def days(self) -> str:
        return f'{self.duration} - days'

    @staticmethod
    def projections() -> list[str]:
        return ['code', 'duration', 'price', 'title', 'location', 'cover_photo']
    
    @staticmethod
    def of(p:Package) -> 'PackageCard':
        return PackageCard(
            code=p.code,
            duration=p.duration,
            price=p.price,
            title=p.title,
            location=p.location.name if not p.location == None else 'Not Defined',
            cover_photo=p.photos.first().path.url if p.photos.exists() else '',
            category=p.category.name
        )