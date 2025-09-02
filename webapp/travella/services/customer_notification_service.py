from dataclasses import dataclass
from datetime import datetime
import uuid
from travella.domains.models.notification_models import CustomerNotification
from travella.domains.models.payment_models import PaymentRequest
from travella.services import image_service


def get_list_by_id(id:uuid) -> list['CustomerNotificationItem']:
    _list = CustomerNotification.objects.filter(customer__id=id).order_by('-created_at')
    return [CustomerNotificationItem.of(i) for i in _list]

@dataclass
class CustomerNotificationItem:
    id:uuid
    message:str
    type:str
    created_at:datetime

    @staticmethod
    def of(n:CustomerNotification) -> 'CustomerNotificationItem':
        return CustomerNotificationItem(
            id=n.id,
            message=n.message,
            type=n.get_type_display(),
            created_at=n.created_at
        )


def save_payment_reject_notification(payment_request:PaymentRequest, reject_message:str, account_id:uuid):
    notification = CustomerNotification(
                id = payment_request.id,
                message = reject_message,
                customer = payment_request.customer,
                type = CustomerNotification.NotificationType.PAYMENT_REJECTED,
                created_by_id = account_id,
            )
    image_service.copy_and_save(_from = payment_request.slip_image, _to = notification.image)
    notification.save()