from django.http import HttpRequest

from travella.domains.models.account_models import Account

def is_exist(username:str) -> bool:
    return Account.objects.filter(email = username).exists()

def get_auth_user(request:HttpRequest) -> Account:
    if request.user.is_authenticated:
        return request.user
    raise RuntimeError('User is not authenticated.')
    