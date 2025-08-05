from django.db import models
from travella.domains.models.abstract_models import AbstractModel
from travella.domains.models.booking_models import Booking
from travella.domains.models.account_models import Account


class ReservedHistory(AbstractModel):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='history')
    reservedBy = models.ForeignKey(Account, on_delete=models.PROTECT)