from dataclasses import dataclass
import uuid

from travella.domains.models.account_models import Account
from travella.domains.models.log_models import AccessLog
from travella.exceptions.business_exception import BusinessException


def get_setting_dtos(id:uuid) -> tuple['AccountInfo', list['AccessLogInfo']]:
    try:
        account:Account = Account.objects.get(id=id)
        logs = AccessLog.objects.filter(account=account).order_by('-created_at')
        return AccountInfo._from(account), [AccessLogInfo._from(log) for log in logs]
    except ValueError as e:
        raise BusinessException(f'Account : {id} not found.')

@dataclass
class AccountInfo:
    email:str
    name:str
    phone:str
    address:str
    photo:str

    @staticmethod
    def _from(a:Account) -> 'AccountInfo':
        return AccountInfo(
            email=a.email,
            name=a.accountdetail.name,
            phone=a.accountdetail.phone,
            address=a.accountdetail.address,
            photo=a.accountdetail.photo.url if a.accountdetail.photo else ''
        )
    

@dataclass
class AccessLogInfo:
    type:str
    status:str
    message:str
    time:str

    @staticmethod
    def _from(log:AccessLog) -> 'AccessLogInfo':
        return AccessLogInfo(
            type=log.get_access_type_display(),
            status=log.get_status_display(),
            message=log.message,
            time=log.created_at,
        )    