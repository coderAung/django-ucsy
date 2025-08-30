from travella.domains.models.account_models import AccountDetail
from travella.services.access_log_service import add_log
from travella.domains.models.log_models import AccessLog
from travella.domains.models.account_models import Account
from travella.domains.models.account_models import AccountManager
import re


def update_detail(account: Account,name=None, phone=None, address=None) -> AccountDetail:
    accountDetail = AccountDetail.objects.get(account=account)
    accountDetail.name = name
    accountDetail.phone = phone
    accountDetail.address = address
    accountDetail.save()
    add_log(
        account=account,
        signin_type=None,
        update_type=AccessLog.UpdateType.INFO_CHANGE.value,
        status=AccessLog.Status.SUCCESS.value,
        message=None
    )
    return accountDetail

def change_password(account: Account,password1=None, password2=None, password3=None) -> Account:
    errors = []
    if not account.check_password(password1):
        print("Password is incorrect!")
        return {"success": False, "errors": "Password is incorrect!"}
    if password2 != password3:
        print("Two new passwords are not the same!")
        return {"success": False, "errors": "Two new passwords are not the same!"}

    if len(password2) < 8:
        return {"success": False, "errors":"Password must be at least 8 characters long"}

    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    if not re.match(pattern, password2):
        return {"success": False, "errors":"Password must contain one uppercase, one lowercase, one number, and one special character"}

    print("Password is correct!")
    account.set_password(password2)
    print(account.set_password(password2))
    account.save()
    add_log(
        account=account,
        signin_type=None,
        update_type=AccessLog.UpdateType.PASSWORD_CHANGE.value,
        status=AccessLog.Status.SUCCESS.value,
        message=None
    )
    return {"success": True, "message": "Password is correct!"}