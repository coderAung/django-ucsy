from django.db import models

from travella.domains.models.abstract_models import AbstractModel
from travella.domains.models.account_models import Account

class AccessLog(AbstractModel):

    class SigninType(models.IntegerChoices):
        SIGN_IN = 1, 'Sign In'
        SIGN_OUT = 2, 'Sign Out'
    class UpdateType(models.IntegerChoices):
        PASSWORD_CHANGE = 1, 'Update Password'
        INFO_CHANGE = 2, 'Update Profile Info'
    class Status(models.IntegerChoices):
        SUCCESS = 1, 'Success'
        FAIL = 2, 'Fail'

    signinType = models.IntegerField(choices=SigninType.choices, null=False, default=0)
    updateType = models.IntegerField(choices=UpdateType.choices, null=False, default=0)
    status = models.IntegerField(choices=Status.choices, null=False, default=1)
    message = models.TextField(null=True)

    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='access_logs')