from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth import login, logout

from travella.dtos.auth_forms import SignInForm
from travella.domains.models.account_models import Account


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
                return redirect(path)
            else:
                return render(request, 'auth/sign-in.html', {'form': form})
    else:
        form = SignInForm()
    return render(request, 'auth/sign-in.html', {'form': form})

@require_POST
def sign_out(request:HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('/auth/sign-in')