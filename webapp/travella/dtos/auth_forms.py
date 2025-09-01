from django import forms
from django.contrib.auth import authenticate
from django.http import HttpRequest

from travella.domains.models.account_models import Account
from travella.exceptions.business_exception import BusinessException
from travella.services import access_log_service, account_service, auth_user


class SignInForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))

    def authenticate_user(self, request:HttpRequest) -> Account:
        data = self.cleaned_data
        email = data['email']
        password = data['password']
        if auth_user.is_exist(email):
            account = authenticate(request, username = email, password = password)
            if account:
                return account
            else:
                form = access_log_service.AccessLogForm.wrong_password_form(password)
                access_log_service.save_log(form, account_service.get_id_by_email(email))
                raise BusinessException(f'Password is wrong.')
        else:
            raise BusinessException(f'User \'{email}\' not found.')