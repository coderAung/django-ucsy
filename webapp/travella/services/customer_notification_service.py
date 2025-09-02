from dataclasses import dataclass
from datetime import datetime
import uuid
from travella.domains.models.booking_history_model import Refunding
from travella.domains.models.booking_models import Booking
from travella.domains.models.notification_models import CustomerNotification
from travella.domains.models.payment_models import PaymentRequest
from travella.exceptions.business_exception import BusinessException
from travella.services import image_service


def get_list_by_id(id:uuid) -> list['CustomerNotificationItem']:
    _list = CustomerNotification.objects.filter(customer__id=id).order_by('-created_at')
    return [CustomerNotificationItem.of(i) for i in _list]

@dataclass
class CustomerNotificationItem:
    id:int
    related_id:uuid
    message:str
    type:str
    created_at:datetime

    @staticmethod
    def of(n:CustomerNotification) -> 'CustomerNotificationItem':
        return CustomerNotificationItem(
            id=n.id,
            related_id=n.related_id,
            message=n.message,
            type=n.get_type_display(),
            created_at=n.created_at
        )


def save_payment_reject_notification(payment_request:PaymentRequest, reject_message:str, account_id:uuid):
    reject_content = f'Your payment request for booking : {payment_request.booking.id} is rejected. \nNote : {reject_message}'
    notification = CustomerNotification(
                related_id = payment_request.id,
                message = reject_content,
                customer = payment_request.customer,
                type = CustomerNotification.NotificationType.PAYMENT_REJECTED,
                created_by_id = account_id,
            )
    image_service.copy_and_save(_from = payment_request.slip_image, _to = notification.image)
    notification.save()

def save_payment_reserved_notification(payment_request:PaymentRequest, account_id:uuid):
    message = f'Your payment for booking : {payment_request.booking.id} is successfully reserved.'
    notification = CustomerNotification(
        related_id=payment_request.id,
        message = message,
        customer = payment_request.customer,
        type = CustomerNotification.NotificationType.PAYMENT_RESERVED,
        created_by_id = account_id
    )
    notification.save()

def save_refund_notification(refund:Refunding):
    message = f'Your booking {refund.booking.id} is cancelled. Refunding is processing.'
    notification = CustomerNotification(
        related_id = refund.id,
        message = message,
        customer = refund.booking.customer,
        type = CustomerNotification.NotificationType.BOOKING_CANCELLED,
        created_by_id = refund.booking.customer.id,
    )
    notification.save()

def get_by_id(id:uuid) -> CustomerNotification:
    try:
        return CustomerNotification.objects.get(id=id)
    except ValueError as e:
        raise BusinessException('Notification not found.')