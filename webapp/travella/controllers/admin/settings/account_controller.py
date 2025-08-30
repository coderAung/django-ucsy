# settings/account/photo POST
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from travella.services.user_service import change_password

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
def password_change(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        password1 = request.POST.get("old_password")
        password2 = request.POST.get("new_password1")
        password3 = request.POST.get("new_password2")
        result = change_password(account=request.user,password1=password1,password2=password2,password3=password3)
        if not result["success"]:
            print(result["errors"])
        else :
            print(result["success"])
    return redirect('/admins/settings/account/password/')