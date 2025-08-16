from datetime import date, timedelta
import uuid
from django.db import models
from django.db.models import Sum

from travella.domains.models.booking_models import Booking
from .abstract_models import AbstractModel
from .account_models import Account


class Category(AbstractModel):
    name = models.CharField(max_length=20, unique=True)
    createdBy = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='categories')

class Location(AbstractModel):
    name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='locations')

class Package(AbstractModel):

    class Transportation(models.IntegerChoices):
        BUS = 1, 'Bus'
        TRAIN = 2, 'Train'
        PLANE = 3, 'Plane'

    class Status(models.TextChoices):
        AVAILABLE = 'Available', 'Available'
        UNAVAILABLE = 'Unavailable', 'Unavailable'
        FINISHED = 'Finished', 'Finished'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=100)
    overview = models.TextField()
    departure = models.DateField()
    duration = models.IntegerField()
    transportation = models.IntegerField(choices=Transportation.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availableTicket = models.IntegerField()

    cover_photo = models.TextField(null=True)
    createdBy = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='packages')
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='packages', null=True)

    @property
    def booking_count(self) -> int:
        result = self.bookings.exclude(status=Booking.Status.CANCELLED).aggregate(total = Sum('ticketCount'))
        return result['total'] or 0
    
    @property
    def status(self) -> 'Package.Status':
        if date.today() >= self.departure:
            return Package.Status.FINISHED
        if self.booking_count < self.availableTicket:
            return Package.Status.AVAILABLE
        else:
            return Package.Status.UNAVAILABLE
        
class Itinerary(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='itineraries')
    day = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['package', 'day'], name='unique_itinerary')
        ]

class Photo(models.Model):
    path = models.ImageField(upload_to='tours/')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='photos')