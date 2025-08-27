from django.db import models
from travella.domains.models.abstract_models import AbstractModel
from travella.domains.models.account_models import Account
from travella.domains.models.booking_models import Booking
from travella.domains.models.payment_models import PaymentRequest


class Reservation(AbstractModel):
    id = models.UUIDField(primary_key=True, editable=False, auto_created=False)
    payment_request = models.OneToOneField(PaymentRequest, null=True, on_delete=models.CASCADE, related_name='reservation')
    booking = models.OneToOneField(Booking, null=True, on_delete=models.CASCADE, related_name='reservation')
    reserved_by = models.ForeignKey(Account, on_delete=models.PROTECT)