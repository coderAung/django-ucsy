import uuid
from travella.domains.models.account_models import Account, AccountDetail
from travella.exceptions.business_exception import BusinessException

def get_id_by_email(email:str) -> uuid:
    try:
        return Account.objects.filter(email = email).values('id').first()['id']
    except ValueError as e:
        raise BusinessException('Account not found')

def update_account_detail(account, dto) -> AccountDetail:
    """Updates the account details based on the provided DTO."""
    detail = AccountDetail.objects.get(account=account)
    detail.name = dto.name
    detail.phone = dto.phone
    detail.address = dto.address

    if dto.profile_image:
        detail.photo = dto.profile_image

    detail.save()
    return detail

def update_account_email(account, new_email: str) -> None:

    account.email = new_email
    account.save()

def update_account_password(account, old_password: str, new_password: str) -> None:

    if account.check_password(old_password):
        account.set_password(new_password)
        account.save()
    else:
        raise BusinessException("Incorrect old password.")
