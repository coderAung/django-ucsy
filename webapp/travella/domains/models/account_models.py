import uuid
from django.db import models
from .abstract_models import AbstractModel

class Account(AbstractModel):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MOD = 'mod', 'Moderator'
        CUSTOMER = 'customer', 'Customer'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Add max_length
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CUSTOMER)


class AccountDetail(AbstractModel):
    name = models.CharField(max_length=100)
    photo = models.URLField(blank=True, null=True)  # Or ImageField if you use media storage
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    account = models.OneToOneField('Account', on_delete=models.CASCADE)
