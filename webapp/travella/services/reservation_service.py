import uuid

from django.db import transaction
from django.core.paginator import Paginator

from travella.domains.models.booking_history_model import Reservation
from travella.domains.models.booking_models import Booking
from travella.domains.models.payment_models import PaymentRequest
from travella.dtos.reservation_dtos import BookingInfo, PackageInfo, PaymentRequestInfo, PaymentRequestItem, Reserver
from travella.dtos.reservation_search import ReservationSearch
from travella.services import payment_request_service
from travella.utils.pagination import PaginationResult


def search_payment_requests(reservation_search:ReservationSearch, page:int) -> PaginationResult:
    _list = PaymentRequest.objects.filter(reservation_search.search()).order_by('-created_at')
    pagination = Paginator(_list, 2)
    result = PaginationResult(page_number=page, pagination=pagination, mapFunc=PaymentRequestItem.of)
    return result

def get_dtos(id:uuid) -> tuple[PaymentRequestInfo, BookingInfo, PackageInfo]:
    payment_request = PaymentRequest.objects.get(id = id)
    booking_info = BookingInfo.of(payment_request.booking)
    package_info = PackageInfo.of(payment_request.booking.package)
    payment_request_info = PaymentRequestInfo(
        reservation_id=payment_request.id,
        payment_type=payment_request.payment_type.name,
        request_datetime=payment_request.created_at,
        total_price=booking_info.total_price,
        slip_image=payment_request.slip_image.url,
        is_reserved=payment_request.is_reserved,
        status=payment_request.booking.get_status_display(),
    )
    return payment_request_info, booking_info, package_info

def reserve(id:uuid, account_id:uuid):
    payment_request = PaymentRequest.objects.get(id=id)
    # start transaction
    with transaction.atomic():
        # save reservation
        reservation = Reservation(
            id=payment_request.id,
            payment_request=payment_request,
            reserved_by_id=account_id
        )
        reservation.save()
        # update payment_request is reserved
        payment_request.is_reserved = True
        payment_request.save()
        # update booking status to requestion to reserved
        payment_request.booking.status = Booking.Status.RESERVED
        payment_request.booking.save()
        # end transaction

def get_reserver(id:uuid) -> Reserver:
    account = Reservation.objects.get(id=id).reserved_by
    return Reserver(
        id=account.id,
        name=account.accountdetail.name,
        email=account.email,
    )