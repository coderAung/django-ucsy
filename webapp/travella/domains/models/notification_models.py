from django.db import models

from travella.domains.models.abstract_models import AbstractModel
from travella.domains.models.account_models import Account


class CustomerNotification(AbstractModel):

    class NotificationType(models.IntegerChoices):
        PAYMENT_REJECTED = 1, 'Payment Rejected'
        PAYMENT_RESERVED = 2, 'Payment Reserved'
        BOOKING_CANCELLED = 3, 'Booking Cancelled'

    related_id = models.UUIDField(null=True)
    message = models.TextField()
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='notifications')
    type = models.IntegerField(choices=NotificationType.choices, null=False)
    image = models.ImageField(upload_to='noti/')
    created_by = models.ForeignKey(Account, on_delete=models.PROTECT, null=True)
