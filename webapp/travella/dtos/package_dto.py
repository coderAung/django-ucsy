import datetime
import decimal
import uuid
from dataclasses import dataclass
from typing import Optional

from ..domains.models.tour_models import Package


@dataclass(frozen=True)
class PackageItem:
    id: uuid.UUID
    code: str
    name: str
    category: str
    duration: int
    departure: datetime.datetime
    group: int
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
            self._group: Optional[int] = None
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

        def group(self, value: int) -> "PackageItem.Builder":
            self._group = value
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
                self._group,
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
                        "group": self._group,
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
                group=self._group,
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
                .group(package.availableTicket)
                .price(package.price)
                .status('Available' if package.availableTicket > 0 else 'Full')
                .bookings(0)
                .build())


@dataclass(frozen=True)
class PackageDetail:
    item: PackageItem
    overview: str
    bookedTicket: int

    def end_in(self):
        return self.item.departure - datetime.timedelta(days=2)

    def departure_end(self) -> datetime:
        return self.item.departure + datetime.timedelta(days=self.item.duration)

    def available_ticket(self) -> int:
        return self.item.group - self.bookedTicket

    @staticmethod
    def of(package:Package) -> 'PackageDetail':
        return (PackageDetail.Builder()
                .item(PackageItem.of(package))
                .overview(package.overview)
                .booked_ticket(0)
                .build())

    class Builder:
        def __init__(self):
            self._item: Optional[PackageItem] = None
            self._overview: Optional[str] = None
            self._bookedTicket: Optional[int] = None

        def item(self, value: PackageItem) -> "PackageDetail.Builder":
            self._item = value
            return self

        def overview(self, value: str) -> "PackageDetail.Builder":
            self._overview = value
            return self

        def booked_ticket(self, value: int) -> "PackageDetail.Builder":
            self._bookedTicket = value
            return self

        def build(self) -> 'PackageDetail':
            missing = [
                name
                for name, val in {
                    "item": self._item,
                    "overview": self._overview,
                    "bookedTicket": self._bookedTicket,
                }.items()
                if val is None
            ]
            if missing:
                raise ValueError(f"Missing fields for PackageDetail: {', '.join(missing)}")

            return PackageDetail(
                item=self._item,  # type: ignore[arg-type]
                overview=self._overview,  # type: ignore[arg-type]
                bookedTicket=self._bookedTicket,  # type: ignore[arg-type]
            )
