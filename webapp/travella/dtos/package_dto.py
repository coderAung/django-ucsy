import datetime
import decimal
import uuid
from dataclasses import dataclass
from typing import List, Optional

from travella.utils.constants import BOOK_BEFORE

from ..domains.models.booking_models import Booking
from ..domains.models.tour_models import Itinerary, Package, PackageData


@dataclass(frozen=True)
class PackageItem:
    id: uuid.UUID
    code: str
    name: str
    category: str
    duration: int
    departure: datetime.datetime
    tickets: int
    status: PackageData.Status
    price: decimal.Decimal
    bookings: int

    @staticmethod
    def of(package:Package) -> 'PackageItem':
        package.data.check_status()
        return (PackageItem.Builder()
                .id(package.id)
                .code(package.code)
                .name(package.title)
                .category(package.category.name)
                .duration(package.duration)
                .departure(package.departure)
                .tickets(package.total_tickets)
                .price(package.price)
                .status(package.data.status)
                .bookings(package.booking_count) #not include CANCELLED bookings
                .build())

    class Builder:
        def __init__(self):
            self._id: Optional[uuid.UUID] = None
            self._code: Optional[str] = None
            self._name: Optional[str] = None
            self._category: Optional[str] = None
            self._duration: Optional[int] = None
            self._departure: Optional[datetime.datetime] = None
            self._ticket: Optional[int] = None
            self._status: Optional[PackageData.Status] = None
            self._price: Optional[decimal.Decimal] = None
            self._bookings: Optional[int] = None

        def id(self, value: uuid.UUID) -> "PackageItem.Builder":
            self._id = value
            return self

        def code(self, value: str) -> "PackageItem.Builder":
            self._code = value
            return self

        def name(self, value: str) -> "PackageItem.Builder":
            self._name = value
            return self

        def category(self, value: str) -> "PackageItem.Builder":
            self._category = value
            return self

        def duration(self, value: int) -> "PackageItem.Builder":
            self._duration = value
            return self

        def departure(self, value: datetime.datetime) -> "PackageItem.Builder":
            self._departure = value
            return self

        def tickets(self, value: int) -> "PackageItem.Builder":
            self._ticket = value
            return self

        def status(self, value: PackageData.Status) -> "PackageItem.Builder":
            self._status = value
            return self

        def price(self, value: decimal.Decimal) -> "PackageItem.Builder":
            self._price = value
            return self

        def bookings(self, value: int) -> "PackageItem.Builder":
            self._bookings = value
            return self

        def build(self) -> "PackageItem":
            # You can add validation here if any field is None
            if None in [
                self._id,
                self._code,
                self._name,
                self._category,
                self._duration,
                self._departure,
                self._ticket,
                self._status,
                self._price,
                self._bookings,
            ]:
                missing = [
                    name for name, val in {
                        "id": self._id,
                        "code": self._code,
                        "name": self._name,
                        "category": self._category,
                        "duration": self._duration,
                        "departure": self._departure,
                        "tickets": self._ticket,
                        "status": self._status,
                        "price": self._price,
                        "bookings": self._bookings,
                    }.items() if val is None
                ]
                raise ValueError(f"Missing fields for PackageItem: {', '.join(missing)}")

            return PackageItem(
                id=self._id,
                code=self._code,
                name=self._name,
                category=self._category,
                duration=self._duration,
                departure=self._departure,
                tickets=self._ticket,
                status=self._status,
                price=self._price,
                bookings=self._bookings,
            )



@dataclass(frozen=True)
class BookingStatus:
    id:uuid
    email:str
    status:str
    ticket_count:int
    bookedAt:datetime

    @staticmethod
    def of(booking:Booking) -> 'BookingStatus':
        return (BookingStatus.Builder()
                .id(booking.id)
                .email(booking.customer.email)
                .status(booking.get_status_display())
                .ticket_count(booking.ticket_count)
                .booked_at(booking.created_at)
                .build())

    class Builder:
        def __init__(self):
            self._id: Optional[uuid.UUID] = None
            self._email: Optional[str] = None
            self._status: Optional[str] = None
            self._ticket_count: Optional[int] = None
            self._booked_at: Optional['datetime.datetime'] = None

        def id(self, value: uuid) -> 'BookingStatus.Builder':
            self._id = value
            return self

        def email(self, value: str) -> 'BookingStatus.Builder':
            self._email = value
            return self

        def status(self, value: str) -> 'BookingStatus.Builder':
            self._status = value
            return self

        def ticket_count(self, value:str) -> 'BookingStatus.Builder':
            self._ticket_count = value
            return self

        def booked_at(self, value: 'datetime') -> 'BookingStatus.Builder':
            self._booked_at = value
            return self

        def build(self) -> 'BookingStatus':
            missing = []
            if self._id is None:
                missing.append('id')
            if self._email is None:
                missing.append('email')
            if self._status is None:
                missing.append('status')
            if self._ticket_count is None:
                missing.append('ticket_count')
            if self._booked_at is None:
                missing.append('booked_at')
            if missing:
                raise ValueError(f'Missing fields for BookingStatus: {", ".join(missing)}')

            return BookingStatus(
                id=self._id,
                email=self._email,  # type: ignore[arg-type]
                status=self._status,  # type: ignore[arg-type]
                ticket_count=self._ticket_count,
                bookedAt=self._booked_at,  # type: ignore[arg-type]
            )


@dataclass
class ItineraryDto:
    day:int
    title:str
    description:str

    @staticmethod
    def of(i:Itinerary) -> 'ItineraryDto':
        return ItineraryDto(i.day, i.title, i.description)

@dataclass(frozen=True)
class PackageItemDetail(PackageItem):
    overview: str
    bookingStatusItems: List['BookingStatus']  # Correct type hint for a list of BookingStatus
    remaining_ticket: int
    itineraries: List['ItineraryDto']

    def end_in(self):
        return self.departure - datetime.timedelta(days=BOOK_BEFORE)

    def departure_end(self) -> datetime.datetime:
        return self.departure + datetime.timedelta(days=self.duration)

    @staticmethod
    def of(package: 'Package') -> 'PackageItemDetail':
        return (PackageItemDetail.Builder()
                .item(PackageItem.of(package))
                .overview(package.overview)
                .remaining_ticket(package.total_tickets - package.booking_count)
                .booking_status_items([BookingStatus.of(b) for b in package.bookings.all()])  # Initialize empty list or some default
                .itineraries([ItineraryDto.of(i) for i in package.itineraries.all()])
                .build())

    class Builder:
        def __init__(self):
            self._item_builder: Optional['PackageItem.Builder'] = None
            self._overview: Optional[str] = None
            self._remaining_ticket: Optional[int] = 0
            self._booking_status_items: Optional[List['BookingStatus']] = None
            self._itineraries: Optional[List['ItineraryDto']] = None

        def item(self, item: 'PackageItem') -> 'PackageItemDetail.Builder':
            self._item_builder = (
                PackageItem.Builder()
                .id(item.id)
                .code(item.code)
                .name(item.name)
                .category(item.category)
                .duration(item.duration)
                .departure(item.departure)
                .tickets(item.tickets)
                .status(item.status)
                .price(item.price)
                .bookings(item.bookings)
            )
            return self

        def from_package(self, package: 'Package') -> 'PackageItemDetail.Builder':
            pkg_item = PackageItem.of(package)
            return self.item(pkg_item)

        def overview(self, value: str) -> 'PackageItemDetail.Builder':
            self._overview = value
            return self
        
        def remaining_ticket(self, value: int) -> 'PackageItemDetail.Builder':
            self._remaining_ticket = value
            return self

        def booking_status_items(self, value: List['BookingStatus']) -> 'PackageItemDetail.Builder':
            self._booking_status_items = value
            return self
        
        def itineraries(self, value: List['ItineraryDto']) -> 'PackageItemDetail.Builder':
            self._itineraries = value
            return self

        def build(self) -> 'PackageItemDetail':
            missing = []
            if self._item_builder is None:
                missing.append('item')
            if self._overview is None:
                missing.append('overview')
            if self._remaining_ticket is None:
                missing.append('remainingTicket')
            if self._booking_status_items is None:
                missing.append('bookingStatusItems')
            if self._itineraries is None:
                missing.append('_itineraries')
            if missing:
                raise ValueError(f'Missing fields for PackageDetail: {", ".join(missing)}')

            item = self._item_builder.build()
            return PackageItemDetail(
                id=item.id,
                code=item.code,
                name=item.name,
                category=item.category,
                duration=item.duration,
                departure=item.departure,
                tickets=item.tickets,
                status=item.status,
                price=item.price,
                bookings=item.bookings,
                overview=self._overview,  # type: ignore[arg-type]
                remaining_ticket=self._remaining_ticket,
                bookingStatusItems=self._booking_status_items,  # type: ignore[arg-type]
                itineraries=self._itineraries
            )
