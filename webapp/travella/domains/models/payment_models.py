import uuid
from django.db import models
from travella.domains.models.abstract_models import AbstractModel
from travella.domains.models.account_models import Account
from travella.domains.models.booking_models import Booking


class PaymentType(AbstractModel):
    name = models.CharField(max_length=50, null=False, unique=True)
    key = models.CharField(max_length=100, null=False)

def populate_payment():
    _count = PaymentType.objects.count()
    if _count == 0:
        PaymentType(name='Kpay', key='098765678').save()
        PaymentType(name='AYA Pay', key='09876545678').save()
        PaymentType(name='CB Pay', key='0945865678').save()

class PaymentRequest(AbstractModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment_request')
    payment_type = models.ForeignKey(PaymentType, on_delete=models.PROTECT, related_name='payment_requests')
    slip_image = models.ImageField(upload_to='slips/')
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='payment_requests')