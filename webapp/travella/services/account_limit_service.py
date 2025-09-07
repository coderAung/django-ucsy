from datetime import date
import uuid

from travella.domains.models.account_models import Account
from travella.domains.models.limit_models import AccountLimit
from travella.exceptions.business_exception import BusinessException


def check_limit(account_id:uuid, type:AccountLimit.Type):
    limit = AccountLimit.objects.filter(account__id=account_id, type=type).first()
    if not limit:
        limit = create_new_limit(account_id, type)
    elif limit.is_expired:
        limit.expire_date = date.today()
        limit.counts = 10
        limit = limit.save()

    if limit.counts > 0:
        consume_limit(limit)
        print(limit.counts)
    else:
        raise BusinessException(f'Your {type.label.lower()} is 0. Limit will be reset tomorrow.')    

def consume_limit(limit:AccountLimit):
    if limit.counts > 0:
        limit.counts = limit.counts - 1
        limit.save()

def create_new_limit(account_id:uuid, type:AccountLimit.Type) -> AccountLimit:
    counts = 10
    if type == AccountLimit.Type.CHAT:
        counts = 100
    limit = AccountLimit(account_id=account_id, type=type, expire_date=date.today(), counts=counts)
    limit.save()
    return limit

def get_limit_counts(account_id:uuid, type:AccountLimit.Type) -> int:
    limit = AccountLimit.objects.filter(account__id=account_id, type=type).first()
    if not limit:
        limit = create_new_limit(account_id, type)
    return limit.counts
