from dataclasses import asdict, dataclass
from datetime import date, time
from typing import Optional
import uuid

from travella.domains.models.booking_models import Booking


@dataclass
class BookingOverview:
    id:uuid
    user:str
    tickets:int
    status:str
    bookedDate:date
    bookedTime:time

    def json(self) -> dict[str, any]:
        return asdict(self)

    @staticmethod
    def of(booking:Booking) -> 'BookingOverview':
        return (BookingOverview.Builder()
                .id(booking.id)
                .user(booking.customer.email)
                .tickets(booking.ticketCount)
                .status(booking.get_status_display())
                .bookedDate(booking.createdAt.date())
                .bookedTime(booking.createdAt.time())
                .build())

    class Builder:
        def __init__(self):
            self._id: Optional[uuid.UUID] = None
            self._user: Optional[str] = None
            self._tickets: Optional[int] = None
            self._status: Optional[Booking.Status] = None
            self._bookedDate: Optional[date] = None
            self._bookedTime: Optional[time] = None
        
        def id(self, value: uuid.UUID) -> 'BookingOverview.Builder':
            self._id = value
            return self

        def user(self, value: str) -> 'BookingOverview.Builder':
            self._user = value
            return self

        def tickets(self, value: int) -> 'BookingOverview.Builder':
            self._tickets = value
            return self

        def status(self, value: 'Booking.Status') -> 'BookingOverview.Builder':
            self._status = value
            return self

        def bookedDate(self, value: date) -> 'BookingOverview.Builder':
            self._bookedDate = value
            return self

        def bookedTime(self, value: time) -> 'BookingOverview.Builder':
            self._bookedTime = value
            return self
        
        def build(self) -> 'BookingOverview':
            return BookingOverview(
                id=self._id,
                user=self._user,
                tickets=self._tickets,
                status=self._status,
                bookedDate=self._bookedDate,
                bookedTime=self._bookedTime,
            )
