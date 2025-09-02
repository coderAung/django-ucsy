from django.http import HttpRequest

from travella.domains.models.account_models import Account, AccountDetail
from travella.exceptions.business_exception import BusinessException


def upload(request:HttpRequest) -> str:
    file = request.FILES['profileImage']
    if not file:
        raise BusinessException('File is empty.')
    if not file.name.endswith(('.jpg', '.png', '.jpeg')):
        raise BusinessException('Invalid image format.')
    account:Account = request.user
    detail:AccountDetail = account.accountdetail
    detail.photo = file
    detail.save()
    return detail.photo.url