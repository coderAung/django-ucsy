from django.db import models

from travella.domains.models.abstract_models import AbstractModel
from travella.domains.models.account_models import Account

class AccessLog(AbstractModel):

    class Type(models.IntegerChoices):
        SIGN_IN = 1, 'Sign In'
        SIGN_UP = 2, 'Sign Up'
        SIGN_OUT = 3, 'Sign Out'
        PASSWORD_CHANGE = 4, 'Update Password'
        INFO_CHANGE = 5, 'Update Profile Info'

    class Status(models.IntegerChoices):
        SUCCESS = 1, 'Success'
        FAIL = 2, 'Fail'
        
    access_type = models.IntegerField(choices=Type.choices, null=True)
    status = models.IntegerField(choices=Status.choices, null=False)
    message = models.TextField(null=True)

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='access_logs')
