from django.db import models
from .abstract_models import AbstractModel
from .account_models import Account


class AccessLog(AbstractModel):

    class Action(models.TextChoices):
        LOG_IN = 'LOG_IN', 'Log In'
        LOG_OUT = 'LOG_OUT', 'Log Out'
        LOGIN_FAILED = 'LOGIN_FAILED', 'Login Failed'
        PASSWORD_CHANGE = 'PASSWORD_CHANGE', 'Password Change'
        PASSWORD_RESET = 'PASSWORD_RESET', 'Password Reset'

    class Status(models.TextChoices):
        SUCCESS = 'SUCCESS', 'Success'
        FAIL = 'FAIL', 'Fail'
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='access_logs'
    )

    action = models.CharField(
        max_length=20,
        choices=Action.choices
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices
    )

    # ip_address = models.GenericIPAddressField(
    #     null=True,
    #     blank=True
    # )

    message = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    def str(self):
        return f"{self.account.email} - {self.get_action_display()} - {self.get_status_display()} at {self.createdAt.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-createdAt']