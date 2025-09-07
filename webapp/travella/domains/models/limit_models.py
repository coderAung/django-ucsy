from datetime import date
from django.db import models

class AccountLimit(models.Model):
    class Type(models.IntegerChoices):
        BOOKING = 1, 'Booking Limit'
        PAYMENT = 2, 'Payment Limit'
        CHAT = 3, 'Chat Limit'
    account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='limit')
    type = models.IntegerField(choices=Type.choices)
    counts = models.IntegerField(default=10)
    expire_date = models.DateField(null=False)

    @property
    def is_expired(self) -> bool:
        return date.today() > self.expire_date