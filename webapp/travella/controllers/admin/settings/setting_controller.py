from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

base = 'admin/settings/'

def view(name:str) -> str:
    return base + name + '.html'

# settings/ GET
def list(request:HttpRequest) -> HttpResponse:
    return render(request, view('list'))

# settings/account GET
def account(request:HttpRequest) -> HttpResponse:
    return render(request, view('account'))

# settings/account/email GET
def email(request:HttpRequest) -> HttpResponse:
    return render(request, view('email-info'))

# settings/account/email GET
def password(request:HttpRequest) -> HttpResponse:
    return render(request, view('password-info'))

# settings/access-logs
def logs(request:HttpRequest) -> HttpResponse:
    return render(request, view('access-logs'))
