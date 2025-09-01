from dataclasses import dataclass
from datetime import date, datetime
import uuid

from django.db import transaction
from django.db.models import Q
from django.http import HttpRequest

from travella.domains.models.booking_history_model import Refunding, Reservation
from travella.domains.models.booking_models import Booking
from travella.domains.models.payment_models import PaymentRequest, PaymentType
from travella.domains.models.tour_models import PackageData
from travella.exceptions.business_exception import BusinessException


# cannot cancelled requesting status booking
# auto cancel pending booking after 24 hours of booking created_at (will not be stored with soft delete)
# can cancel pending booking
# can cancel reserved booking
# if reserved booking is cancelled before deadline, the fund is refunded
# to refund, a refund voucher will be printed to user
def cancel_booking(id:uuid):
    # get booking
    try:
        with transaction.atomic():
            booking = Booking.objects.get(id=id)
            booking_status = Booking.Status(booking.status)
            
            if booking_status == Booking.Status.REQUESTING:
                raise BusinessException('Payment requesting booking cannot be cancelled.')
            if booking_status == Booking.Status.CANCELLED:
                raise BusinessException('Cancelled booking cannot be cancelled.')

            # change status to cancelled
            if booking_status == Booking.Status.RESERVED:
                reservation:Reservation = booking.reservation
                if reservation.is_refundable:
                    raise BusinessException('Booking is refundable.')
                cancel_pending_booking(booking)
            if booking_status == Booking.Status.PENDING:
                cancel_pending_booking(booking)            
            # update package data => status, remaining ticket
            update_remaing_tickets(booking)

    except ValueError as e:
        raise BusinessException(f'Booking not found. (id:{id})')

def update_remaing_tickets(booking:Booking):
    ticket_count = booking.ticket_count
    package_data:PackageData = booking.package.data
    remaining_tickets = package_data.remaining_tickets
    package_data.remaining_tickets = remaining_tickets + ticket_count
    package_data.save()

def cancel_pending_booking(booking:Booking):
    booking.status = Booking.Status.CANCELLED
    booking.status_updated_at = datetime.now()
    booking.save()

def is_refundable(id:uuid) -> bool:
    try:
        booking = Booking.objects.get(id = id)
        booking_status = Booking.Status(booking.status)
        if booking_status == Booking.Status.RESERVED:
            reservation:Reservation = booking.reservation
            return reservation.is_refundable
        else:
            return False
    except ValueError as e:
        raise BusinessException('Booking not found')

def cancel_refundable_booking(form:'RefundForm'):
    try:
        booking = Booking.objects.get(id=form.booking_id)
        with transaction.atomic():
            form.get_model().save()
            cancel_pending_booking(booking)
            update_remaing_tickets(booking)
    except ValueError as e:
        raise BusinessException('Unknown Error')

class RefundForm:
    booking_id:uuid
    refund_payment_type:str
    refund_phone: str

    def __init__(self, booking_id:uuid, request:HttpRequest):
        self.booking_id = booking_id
        self.refund_payment_type = request.POST.get('refundPaymentType')
        self.refund_phone = request.POST.get('refundPaymentPhone')
    
    def get_model(self) -> Refunding:
        return Refunding(
            id=self.booking_id,
            booking_id=self.booking_id,
            refund_phone=self.refund_phone,
            refund_payment_type=self.refund_payment_type
        )

def auto_cancel_pending_bookings():
    q = Q(status=Booking.Status.PENDING, auto_cancel_date__gte=datetime.today())
    q |= Q(auto_cancel_date = None)
    bookings_to_auto_cancel = Booking.objects.filter(q)
    if bookings_to_auto_cancel.count() > 0:
        print('========== Auto Deleting Pending Bookings ============')
        bookings_to_auto_cancel.delete()