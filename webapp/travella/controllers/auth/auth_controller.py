from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth import login, logout

from travella.dtos.auth_forms import SignInForm
from travella.domains.models.account_models import Account
from travella.domains.models.log_models import AccessLog
from travella.services.access_log_service import add_log


def sign_in(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = form.authenticate_user(request)
            if user:
                login(request, user)
                path = ''
                if user.role == Account.Role.ADMIN or user.role == Account.Role.MOD:
                    path = '/admins/dashboard'
                else:
                    path = '/customers/home'
                add_log(
                    account=request.user,
                    signin_type=AccessLog.SigninType.SIGN_IN.value,
                    update_type=None,
                    status=AccessLog.Status.SUCCESS.value,
                    message=None
                )
                return redirect(path)
            else:
                return render(request, 'auth/sign-in.html', {'form': form})
    else:
        form = SignInForm()
    return render(request, 'auth/sign-in.html', {'form': form})

@require_POST
def sign_out(request:HttpRequest) -> HttpResponse:
    add_log(
        account=request.user,
        signin_type=AccessLog.SigninType.SIGN_OUT.value,
        update_type=None,
        status=AccessLog.Status.SUCCESS.value,
        message=None
    )
    logout(request)
    return redirect('/auth/sign-in')