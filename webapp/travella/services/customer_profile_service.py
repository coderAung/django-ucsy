from dataclasses import dataclass
import uuid
from django.http import HttpRequest

from travella.domains.models.account_models import Account, AccountDetail
from travella.domains.models.booking_models import Booking
from travella.domains.models.tour_models import Package, PackageData


def get_profile_data(request:HttpRequest) -> 'AccountDto':
    account:Account = request.user
    detail:AccountDetail = account.accountdetail
    return AccountDto(
        profile_image=detail.photo.url if detail.photo else '',
        phone=detail.phone,
        address=detail.address,
        name=detail.name,
        id=account.id,
        email=account.email,
        created_at=account.created_at,
    )

def get_tour_reminders_by_account_id(id:uuid) -> list[str]:
    return [
        reminder_message(b) 
        for b in Booking.objects.filter(
            customer__id=id, status=Booking.Status.RESERVED)
            .exclude(package__data__status = PackageData.Status.FINISHED)]

def reminder_message(b:Booking) -> str:
    package:Package = b.package
    return f'Your tour is schedule for {package.departure}. Please be prepared for you upcomint trip \'{package.title}\''

def get_booking_status_by_account_id(id:uuid) -> 'BookingStatusDto':
    _list = Booking.objects.filter(customer__id=id)
    reserved_bookings = 0
    requesting_bookings = 0
    pending_bookings = 0
    cancelled_bookings = 0
    for i in _list:
        if i.status == Booking.Status.RESERVED.value:
            reserved_bookings += 1
        if i.status == Booking.Status.REQUESTING.value:
            requesting_bookings += 1
        if i.status == Booking.Status.PENDING.value:
            pending_bookings += 1
        if i.status == Booking.Status.CANCELLED.value:
            cancelled_bookings += 1
    return BookingStatusDto(
        reserved_bookings=reserved_bookings,
        requesting_bookings=requesting_bookings,
        pending_bookings=pending_bookings,
        cancelled_bookings=cancelled_bookings
    )

@dataclass
class BookingStatusDto:
    reserved_bookings:int
    requesting_bookings:int
    pending_bookings:int
    cancelled_bookings:int

@dataclass
class AccountDto:
    profile_image:str
    email:str
    name:str
    phone:str
    address:str
    id:uuid
    created_at:str


def update(id:uuid, name:str, phone:str, address:str):
    detail = AccountDetail.objects.get(account_id=id)
    detail.name = name
    detail.phone = phone
    detail.address = address
    detail.save()
