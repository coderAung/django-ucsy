from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from travella.dtos.settings.account_staff_dto import AccountDetailDTO
from travella.services.account_service import update_account_detail, update_account_email, update_account_password
from django.http import JsonResponse

base = 'admin/settings/'

def view(name: str) -> str:
    return base + name + '.html'

@require_POST
def info(request: HttpRequest) -> HttpResponse:
    account = request.user
    
    dto = AccountDetailDTO(
        name=request.POST.get('name', ''),
        phone=request.POST.get('phone', ''),
        address=request.POST.get('address', ''),
        profile_image=request.FILES.get('profile_image')
    )
    
    update_account_detail(account, dto)
    return redirect('/admins/settings/account')

@require_POST
def email(request: HttpRequest) -> HttpResponse:
    account = request.user
    new_email = request.POST.get('new_email', '')

    try:
        update_account_email(account, new_email)
        return redirect('/admins/settings/account/email/')
    except Exception as e:
        return redirect('/admins/settings/account/email/')
    
@require_POST
def password(request: HttpRequest) -> HttpResponse:
    account = request.user
    old_password = request.POST.get('old_password', '')
    new_password1 = request.POST.get('new_password1', '')
    new_password2 = request.POST.get('new_password2', '')

    if new_password1 != new_password2:
        # return redirect('/admins/settings/account/password/')
        return JsonResponse({"error": "Passwords do not match"}, status=400)


    try:
        update_account_password(account, old_password, new_password1)
    except Exception:
        # return redirect('/admins/settings/account/password/')
        return JsonResponse({"error": "Incorrect old password"}, status=400)


    # return redirect('/admins/settings/account/password/')
    return JsonResponse({"success": "Password changed successfully", "redirect": "/admins/settings/account/password/"})
