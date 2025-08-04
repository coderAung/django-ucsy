from ..domains.models.account_models import Account
from django.contrib.auth.hashers import check_password

def login_user(email: str, raw_password: str):
    try:
        account = Account.objects.get(email=email, role='admin')
        if check_password(raw_password, account.password):
            return True, account
        else:
            return False, 'Invalid password.'
    except Account.DoesNotExist:
        return False, 'No account found with this email.'
