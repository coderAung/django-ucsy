# settings/account/photo POST
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST


base = 'admin/settings/'

def view(name:str) -> str:
    return base + name + '.html'

# settings/account/photo POST
def photo(request:HttpRequest) -> HttpResponse:
    return redirect('/admins/settings/account')

# settings/account/info POST
def info(request:HttpRequest) -> HttpResponse:
    return redirect('/admins/settings/account')

# settings/account/email/chage POST
def email(request:HttpRequest) -> HttpResponse:
    return redirect('/admins/settings/account/email')

# settings/account/password/change POST
@require_POST
def password(request:HttpRequest) -> HttpResponse:
    return redirect('/admins/settings/account/password')
