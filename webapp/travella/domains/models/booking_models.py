from datetime import datetime
import uuid
from django.db import models
from django.utils import timezone
from django.db.models import Max

from travella.exceptions.business_exception import BusinessException
from .abstract_models import AbstractModel

class Booking(AbstractModel):
    class Status(models.IntegerChoices):
        PENDING = 1, 'Pending'
        RESERVED = 2, 'Reserved'
        CANCELLED = 3, 'Cancelled'
        REQUESTING = 4, 'Requesting'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking_code = models.CharField(max_length=20, unique=True, editable=False, null=True)  # new field
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    ticket_count = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    status_updated_at = models.DateTimeField(auto_now=True)

    phone = models.CharField(max_length=20, null=True, blank=True)
    
    package = models.ForeignKey('Package', on_delete=models.PROTECT, related_name='bookings')
    customer = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='bookings')
    auto_cancel_date = models.DateTimeField(null=True)

    @property
    def is_cancellable(self):
        if self.auto_cancel_date:
            return timezone.now() <= self.auto_cancel_date
        raise BusinessException('Auto Cancel Date is None.')

    def save(self, *args, **kwargs):
        # Generate booking code only on create
        if not self.booking_code:
            today_str = datetime.now().strftime("%Y%m%d")

            # Find the last booking today
            last_code = Booking.objects.filter(
                booking_code__startswith=f"BKG-{today_str}"
            ).aggregate(Max("booking_code"))["booking_code__max"]

            if last_code:
                # Extract running number and increment
                last_number = int(last_code.split("-")[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.booking_code = f"BKG-{today_str}-{new_number:04d}"

        super().save(*args, **kwargs)
