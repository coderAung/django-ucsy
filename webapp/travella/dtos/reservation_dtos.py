from dataclasses import dataclass
from datetime import date, time, timedelta
import uuid

from django.http import HttpRequest, QueryDict
from django.core.files.uploadedfile import UploadedFile
from django.utils.datastructures import MultiValueDict

from travella.domains.models.booking_models import Booking
from travella.domains.models.payment_models import PaymentRequest
from travella.domains.models.tour_models import Package


@dataclass
class PackageInfo:
    code:str
    title:str
    category:str
    departure_from:date
    departure_to:date
    duration:int
    unit_price:float

    @staticmethod
    def of(p:Package) -> 'PackageInfo':
        return PackageInfo(
            code=p.code,
            title=p.title,
            category=p.category.name,
            departure_from=p.departure,
            duration=p.duration,
            departure_to=(p.departure + timedelta(p.duration)),
            unit_price=p.price
        )
    
@dataclass
class BookingInfo:
    id:uuid
    booking_date:date
    booking_time:time
    ticket_count:int
    unit_price:float
    email:str
    name:str

    def total_price(self) -> float:
        return self.unit_price * self.ticket_count
    
    @staticmethod
    def of(b:Booking) -> 'BookingInfo':
        return BookingInfo(
            id=b.id,
            booking_date=b.created_at.date(),
            booking_time=b.created_at.time(),
            ticket_count=b.ticket_count,
            unit_price=b.unit_price,
            email=b.customer.email,
            name=b.customer.accountdetail.name,
        )

@dataclass
class PaymentRequestForm:
    booking_id:int
    payment:str
    slip_image:UploadedFile
    
    @staticmethod
    def of(post:QueryDict, files:MultiValueDict) -> 'PaymentRequestForm':
        form = PaymentRequestForm(
            booking_id=post.get('bookingId'),
            payment=post.get('payment'),
            slip_image=files.get('slipImage')
        )
        return form