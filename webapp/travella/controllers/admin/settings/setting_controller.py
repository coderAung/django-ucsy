from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from travella.domains.models.account_models import AccountDetail
from travella.services.user_service import update_detail

base = 'admin/settings/'

def view(name:str) -> str:
    return base + name + '.html'

# settings/ GET
def list(request:HttpRequest) -> HttpResponse:
    return render(request, view('list'))

# settings/account GET
def account(request:HttpRequest) -> HttpResponse:
    try:
        account_detail = AccountDetail.objects.get(account=request.user)
    except AccountDetail.DoesNotExist:
        account_detail = None  # or create empty

    context = {
        "account_detail": account_detail
    }
    return render(request, view('account'), context)

# settings/account/email GET
def email(request:HttpRequest) -> HttpResponse:
    return render(request, view('email-info'))

# settings/account/email GET
def password(request:HttpRequest) -> HttpResponse:
    return render(request, view('password-info'))

# settings/access-logs
def logs(request:HttpRequest) -> HttpResponse:
    return render(request, view('access-logs'))

@require_POST
def update_profile(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        update_detail(account=request.user,name=name, phone=phone, address=address)
    return redirect('/admins/settings/account/')