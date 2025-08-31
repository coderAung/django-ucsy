from datetime import date
from django.db import models
from travella.domains.models.abstract_models import AbstractModel
from travella.domains.models.account_models import Account
from travella.domains.models.booking_models import Booking
from travella.domains.models.payment_models import PaymentRequest, PaymentType


class Reservation(AbstractModel):
    id = models.UUIDField(primary_key=True, editable=False, auto_created=False)
    payment_request = models.OneToOneField(PaymentRequest, null=True, on_delete=models.CASCADE, related_name='reservation')
    booking = models.OneToOneField(Booking, null=True, on_delete=models.CASCADE, related_name='reservation')
    reserved_by = models.ForeignKey(Account, on_delete=models.PROTECT)
    refund_cover_date = models.DateField(null=True)

    @property
    def is_refundable(self) -> bool:
        return date.today() <= self.refund_cover_date

class Refunding(AbstractModel):
    # booking_id
    id = models.UUIDField(primary_key=True, editable=False, auto_created=False)
    booking = models.OneToOneField(Booking, null=True, on_delete=models.CASCADE, related_name='refund')
    refund_phone = models.CharField(max_length=15, null=False)
    refund_payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, related_name='refundings')