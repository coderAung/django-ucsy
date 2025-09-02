import uuid

from django.db import transaction

from travella.domains.models.account_models import Account, AccountDetail
from travella.exceptions.business_exception import BusinessException


def delete(id:uuid, password:str):
    try:
        account = Account.objects.get(id=id)
        if account.check_password(password):
            raise BusinessException('Incorrect password.')
        with transaction.atomic():
            detail:AccountDetail = account.accountdetail
            detail.photo.delete()
            detail.delete()
            account.delete()
    except ValueError as e:
        raise BusinessException('Account not found.')