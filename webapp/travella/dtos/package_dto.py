import datetime
import decimal
import uuid
from dataclasses import dataclass
from typing import List, Optional

from ..domains.models.booking_models import Booking
from ..domains.models.tour_models import Package


@dataclass(frozen=True)
class PackageItem:
    id: uuid.UUID
    code: str
    name: str
    category: str
    duration: int
    departure: datetime.datetime
    tickets: int
    status: str
    price: decimal.Decimal
    bookings: int

    class Builder:
        def __init__(self):
            self._id: Optional[uuid.UUID] = None
            self._code: Optional[str] = None
            self._name: Optional[str] = None
            self._category: Optional[str] = None
            self._duration: Optional[int] = None
            self._departure: Optional[datetime.datetime] = None
            self._ticket: Optional[int] = None
            self._status: Optional[str] = None
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

        def status(self, value: str) -> "PackageItem.Builder":
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

    @staticmethod
    def of(package:Package) -> 'PackageItem':
        return (PackageItem.Builder()
                .id(package.id)
                .code(package.code)
                .name(package.title)
                .category(package.category.name)
                .duration(package.duration)
                .departure(package.departure)
                .tickets(package.availableTicket)
                .price(package.price)
                .status('Available' if package.availableTicket > 0 else 'Full')
                .bookings(package.bookings.count())
                .build())


@dataclass(frozen=True)
class BookingStatus:
    email:str
    status:str
    bookedAt:datetime

    @staticmethod
    def of(booking:Booking) -> 'BookingStatus':
        return (BookingStatus.Builder()
                .email(booking.customer.email)
                .status(booking.get_status_display())
                .booked_at(booking.createdAt)
                .build())

    class Builder:
        def __init__(self):
            self._email: Optional[str] = None
            self._status: Optional[str] = None
            self._booked_at: Optional['datetime'] = None

        def email(self, value: str) -> 'BookingStatus.Builder':
            self._email = value
            return self

        def status(self, value: str) -> 'BookingStatus.Builder':
            self._status = value
            return self

        def booked_at(self, value: 'datetime') -> 'BookingStatus.Builder':
            self._booked_at = value
            return self

        def build(self) -> 'BookingStatus':
            missing = []
            if self._email is None:
                missing.append('email')
            if self._status is None:
                missing.append('status')
            if self._booked_at is None:
                missing.append('bookedAt')
            if missing:
                raise ValueError(f'Missing fields for BookingStatus: {", ".join(missing)}')

            return BookingStatus(
                email=self._email,  # type: ignore[arg-type]
                status=self._status,  # type: ignore[arg-type]
                bookedAt=self._booked_at,  # type: ignore[arg-type]
            )


@dataclass(frozen=True)
class PackageDetail(PackageItem):
    overview: str
    bookingStatusItems: List['BookingStatus']  # Correct type hint for a list of BookingStatus

    def end_in(self):
        return self.departure - datetime.timedelta(days=2)

    def departure_end(self) -> datetime.datetime:
        return self.departure + datetime.timedelta(days=self.duration)

    def remaining_ticket(self) -> int:
        return self.tickets - self.bookings

    @staticmethod
    def of(package: 'Package') -> 'PackageDetail':
        return (PackageDetail.Builder()
                .item(PackageItem.of(package))
                .overview(package.overview)
                .booking_status_items([BookingStatus.of(b) for b in package.bookings.all()])  # Initialize empty list or some default
                .build())

    class Builder:
        def __init__(self):
            self._item_builder: Optional['PackageItem.Builder'] = None
            self._overview: Optional[str] = None
            self._booking_status_items: Optional[List['BookingStatus']] = None

        def item(self, item: 'PackageItem') -> 'PackageDetail.Builder':
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

        def from_package(self, package: 'Package') -> 'PackageDetail.Builder':
            pkg_item = PackageItem.of(package)
            return self.item(pkg_item)

        def overview(self, value: str) -> 'PackageDetail.Builder':
            self._overview = value
            return self

        def booking_status_items(self, value: List['BookingStatus']) -> 'PackageDetail.Builder':
            self._booking_status_items = value
            return self

        def build(self) -> 'PackageDetail':
            missing = []
            if self._item_builder is None:
                missing.append('item')
            if self._overview is None:
                missing.append('overview')
            if self._booking_status_items is None:
                missing.append('bookingStatusItems')
            if missing:
                raise ValueError(f'Missing fields for PackageDetail: {", ".join(missing)}')

            item = self._item_builder.build()
            return PackageDetail(
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
                bookingStatusItems=self._booking_status_items,  # type: ignore[arg-type]
            )
