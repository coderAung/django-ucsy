import uuid

from travella.domains.models.account_models import Account
from travella.exceptions.business_exception import BusinessException


def get_id_by_email(email:str) -> uuid:
    try:
        return Account.objects.filter(email = email).values('id').first()['id']
    except ValueError as e:
        raise BusinessException('Account not found')