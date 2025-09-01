from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth import login, logout
from django.contrib import messages

from travella.domains.models.log_models import AccessLog
from travella.dtos.auth_forms import SignInForm
from travella.domains.models.account_models import Account
from travella.exceptions.business_exception import BusinessException
from travella.services import access_log_service, auth_user
from travella.services.access_log_service import AccessLogForm
from travella.services.package_utils import is_empty


def sign_in(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            try:
                user = form.authenticate_user(request)
                if user:
                    login(request, user)
                    path = ''
                    if user.role == Account.Role.ADMIN or user.role == Account.Role.MOD:
                        path = '/admins/dashboard'
                    else:
                        path = '/public/discover'
                    if not is_empty(request.GET.get('next')):
                        path = request.GET.get('next')
                    form = AccessLogForm.sign_in_success_form()
                    access_log_service.save_log(form, request.user.id)
                    return redirect(path)
            except BusinessException as e:
                messages.error(request, e.get_message())
                return render(request, 'auth/sign-in.html', {'form': form})
    else:
        form = SignInForm()
    return render(request, 'auth/sign-in.html', {'form': form})

@require_POST
def sign_out(request:HttpRequest) -> HttpResponse:
    access_log_service.save_log(AccessLogForm.sign_out_success_form(), request.user.id)
    logout(request)
    return redirect('/auth/sign-in')