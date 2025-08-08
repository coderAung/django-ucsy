from django.db import models

from travella.domains.models.abstract_models import AbstractModel
from travella.domains.models.account_models import Account

class AccessLog(AbstractModel):

    class Type(models.IntegerChoices):
        SIGN_IN = 1, 'Sign In'
        SIGN_UP = 2, 'Sign Up'
    class Status(models.IntegerChoices):
        SUCCESS = 1, 'Success'
        FAIL = 2, 'Fail'
        
    type = models.IntegerField(choices=Type.choices, null=False)
    status = models.IntegerField(choices=Status.choices, null=False)
    message = models.TextField(null=True)

    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='access_logs')

class ProfileEditLog(AbstractModel):
    class Type(models.IntegerChoices):
        EMAIL_CHANGE = 1, 'Update Email'
        PASSWORD_CHANGE = 2, 'Update Password'
        INFO_CHANGE = 3, 'Update Profile Info'
    
    class Status(models.IntegerChoices):
        SUCCESS = 1, 'Suceess'
        FAIL = 2, 'Fail'
    
    type = models.IntegerField(choices=Type.choices, null=False)
    status = models.IntegerField(choices=Status.choices, null=False)
    message = models.TextField(null=True)