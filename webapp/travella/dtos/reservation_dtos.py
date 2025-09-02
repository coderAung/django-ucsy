from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
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
    location:str
    transportation:str
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
            location=p.location.name if not p.location == None else 'Not defined',
            transportation=p.get_transportation_display(),
            unit_price=p.price
        )
    
@dataclass
class BookingInfo:
    id:uuid
    booking_code:str
    booking_date:date
    booking_time:time
    ticket_count:int
    unit_price:float
    email:str
    name:str
    phone:str

    def total_price(self) -> float:
        return self.unit_price * self.ticket_count
    
    @staticmethod
    def of(b:Booking) -> 'BookingInfo':
        return BookingInfo(
            id=b.id,
            booking_code=b.booking_code,
            booking_date=b.created_at.date(),
            booking_time=b.created_at.time(),
            ticket_count=b.ticket_count,
            unit_price=b.unit_price,
            email=b.customer.email,
            name=b.customer.accountdetail.name,
            phone=b.customer.accountdetail.phone,
        )

@dataclass
class PaymentRequestInfo:
    reservation_id:uuid
    code:str
    payment_type:str
    request_datetime:datetime
    total_price:float
    slip_image:str
    is_reserved:bool
    status:str

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

@dataclass
class PaymentRequestItem:
    email:str
    name:str
    phone:str
    booking_id:uuid
    booking_code:str
    booking_date:date
    request_date:date
    status:str
    payment_type:str
    reservation_id:uuid
    code:str

    @staticmethod
    def of(p:PaymentRequest) -> 'PaymentRequestItem':
        return PaymentRequestItem(
            email=p.customer.email,
            name=p.customer.accountdetail.name,
            phone=p.customer.accountdetail.phone,
            booking_id=p.booking.id,
            booking_code=p.booking.booking_code,
            booking_date=p.booking.created_at.date,
            request_date=p.created_at.date,
            status=p.booking.get_status_display(),
            payment_type=p.payment_type.name,
            reservation_id=p.id,
            code=p.code,
        )
    
@dataclass
class Reserver:
    id:uuid
    name:str
    email:str
    reserved_at:datetime