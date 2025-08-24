import uuid
from django.db import models
from .abstract_models import AbstractModel

class Booking(AbstractModel):

    objects = None

    class Status(models.IntegerChoices):
        PENDING = 1, 'Pending'
        RESERVED = 2, 'Reserved'
        CANCELLED = 3, 'Cancelled'
        REQUESTING = 4, 'Requesting'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    ticket_count = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    status_updated_at = models.DateTimeField(auto_now=True)
    
    package = models.ForeignKey('Package', on_delete=models.PROTECT, related_name='bookings')
    customer = models.ForeignKey('Account', on_delete=models.PROTECT, related_name='bookings')
