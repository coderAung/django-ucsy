import uuid
from django.db import models
from django.utils.crypto import get_random_string
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
    code = models.CharField(max_length=20, unique=True, editable=False, null=True)  # renamed field
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment_request')
    payment_type = models.ForeignKey(PaymentType, on_delete=models.PROTECT, related_name='payment_requests')
    slip_image = models.ImageField(upload_to='slips/')
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='payment_requests')
    is_reserved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Generate code if not set
        if not self.code:
            self.code = "PAY-" + get_random_string(6).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code
