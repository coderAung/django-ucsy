from travella.domains.models.log_models import AccessLog
from travella.domains.models.account_models import Account


def add_log(account: Account, signin_type=None, update_type=None, status=None, message=None) -> AccessLog:
    log = AccessLog(
        account=account,
        signinType=signin_type if signin_type else 0,
        updateType=update_type if update_type else 0,
        status=status,
        message=message
    )
    log.save()
    return log