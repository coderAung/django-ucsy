import datetime
import decimal
import uuid
from dataclasses import dataclass
from typing import List

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
    remaining_tickets: int
    is_deletable:bool

    @staticmethod
    def of(package: Package) -> "PackageItem":
        package.data.check_status()
        return PackageItem(
            id=package.id,
            code=package.code,
            name=package.title,
            category=package.category.name,
            duration=package.duration,
            departure=package.departure,
            tickets=package.total_tickets,
            status=package.data.status,
            price=package.price,
            bookings=package.booking_count,
            remaining_tickets=package.data.remaining_tickets,
            is_deletable=package.is_deletable,
        )


@dataclass(frozen=True)
class BookingStatus:
    id: uuid.UUID
    email: str
    status: str
    ticket_count: int
    bookedAt: datetime.datetime

    @staticmethod
    def of(booking: Booking) -> "BookingStatus":
        return BookingStatus(
            id=booking.id,
            email=booking.customer.email,
            status=booking.get_status_display(),
            ticket_count=booking.ticket_count,
            bookedAt=booking.created_at,
        )


@dataclass(frozen=True)
class ItineraryDto:
    day: int
    title: str
    description: str

    @staticmethod
    def of(i: Itinerary) -> "ItineraryDto":
        return ItineraryDto(
            day=i.day,
            title=i.title,
            description=i.description,
        )


@dataclass(frozen=True)
class PackageItemDetail(PackageItem):
    overview: str
    bookingStatusItems: List[BookingStatus]
    itineraries: List[ItineraryDto]

    def end_in(self) -> datetime.datetime:
        return self.departure - datetime.timedelta(days=BOOK_BEFORE)

    def departure_end(self) -> datetime.datetime:
        return self.departure + datetime.timedelta(days=self.duration)

    @staticmethod
    def of(package: Package) -> "PackageItemDetail":
        base_item = PackageItem.of(package)
        return PackageItemDetail(
            id=base_item.id,
            code=base_item.code,
            name=base_item.name,
            category=base_item.category,
            duration=base_item.duration,
            departure=base_item.departure,
            tickets=base_item.tickets,
            status=base_item.status,
            price=base_item.price,
            bookings=base_item.bookings,
            is_deletable=base_item.is_deletable,
            remaining_tickets=package.data.remaining_tickets,
            overview=package.overview,
            bookingStatusItems=[BookingStatus.of(b) for b in package.bookings.all()],
            itineraries=[ItineraryDto.of(i) for i in package.itineraries.all()],
        )
