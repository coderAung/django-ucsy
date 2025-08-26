import uuid
from travella.domains.models.booking_models import Booking
from travella.domains.models.payment_models import PaymentRequest
from travella.dtos.reservation_dtos import BookingInfo, PackageInfo, PaymentRequestInfo, PaymentRequestItem
from travella.services import payment_request_service


def search_payment_requests() -> list[PaymentRequestItem]:
    _list = PaymentRequest.objects.filter(booking__status=Booking.Status.REQUESTING).order_by('-created_at')
    return [PaymentRequestItem.of(l) for l in _list]

def get_dtos(id:uuid) -> tuple[PaymentRequestInfo, BookingInfo, PackageInfo]:
    payment_request = PaymentRequest.objects.get(id = id)
    booking_info = BookingInfo.of(payment_request.booking)
    package_info = PackageInfo.of(payment_request.booking.package)
    payment_request_info = PaymentRequestInfo(
        reservation_id=payment_request.id,
        payment_type=payment_request.payment_type.name,
        request_datetime=payment_request.created_at,
        total_price=booking_info.total_price,
        slip_image=payment_request.slip_image.url
    )
    return payment_request_info, booking_info, package_info