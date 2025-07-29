import uuid
from django.db import models
from .abstract_models import AbstractModel
from .account_models import Account


class Category(AbstractModel):
    name = models.CharField(max_length=20, unique=True)
    createdBy = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='categories')


class Package(AbstractModel):

    class Transportation(models.IntegerChoices):
        BUS = 1, 'Bus'
        PLANE = 2, 'Plane'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=100)
    overview = models.TextField()
    departure = models.DateField()
    duration = models.IntegerField()
    transportation = models.IntegerField(choices=Transportation.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availableTicket = models.IntegerField()

    createdBy = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='packages')


class Itinerary(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='itineraries')
    day = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['package', 'day'], name='unique_itinerary')
        ]
