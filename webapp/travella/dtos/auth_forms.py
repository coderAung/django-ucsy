from django import forms
from django.contrib.auth import authenticate
from django.http import HttpRequest

from travella.domains.models.account_models import Account


class SignInForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))

    def authenticate_user(self, request:HttpRequest) -> Account:
        data = self.cleaned_data
        email = data['email']
        password = data['password']
        account = authenticate(request, username = email, password = password)
        print(account)
        return account