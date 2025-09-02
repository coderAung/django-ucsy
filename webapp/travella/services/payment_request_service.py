import uuid

from django.db import transaction

from travella.domains.models.account_models import Account
from travella.domains.models.booking_models import Booking
from travella.domains.models.payment_models import PaymentRequest, PaymentType, populate_payment
from travella.dtos.reservation_dtos import BookingInfo, PackageInfo, PaymentRequestForm
from travella.exceptions.business_exception import BusinessException


def load_payments() -> PaymentType:
    populate_payment()
    return PaymentType.objects.all()

def get_by_id(id:uuid) -> PaymentRequest:
    try:
        return PaymentRequest.objects.get(id=id)
    except ValueError as e:
        raise BusinessException('Payment not found.')

def get_reservation_dtos(booking_id:uuid, customer_id:uuid) -> tuple[PackageInfo, BookingInfo]:
    booking = Booking.objects.get(id=booking_id)
    payment_request_count = PaymentRequest.objects.filter(booking__id = booking_id).count()
    if payment_request_count != 0:
        raise BusinessException(f'Booking is requesting payment and cannot be request again.')
    status = Booking.Status(booking.status)
    if status == Booking.Status.PENDING:
        return PackageInfo.of(booking.package), BookingInfo.of(booking)
    raise BusinessException(f'Booking is {status.label} and cannot be request payment.')

def is_authorize(booking_id:uuid, customer_id:uuid) -> bool:
    return Booking.objects.get(id = booking_id).customer.id == customer_id

def save(customer_id:uuid, form:PaymentRequestForm):
    booking = Booking.objects.get(id = form.booking_id)
    payment_type = PaymentType.objects.get(name = form.payment)
    customer = Account.objects.get(id = customer_id)
    with transaction.atomic():
        model = PaymentRequest(
            booking=booking,
            payment_type=payment_type,
            slip_image=form.slip_image,
            customer=customer
        )
        model.save()
        booking.status = Booking.Status.REQUESTING
        booking.save()
