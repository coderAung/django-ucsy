from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from ....domains.models.account_models import Account
from ....domains.forms.signIn import AdminLoginForm
from ....services.auth_service import login_user
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            success, account_or_msg = login_user(email, password)
            if success:
                request.session['admin_id'] = str(account_or_msg.id)
                return redirect('dashboard')
            else:
                messages.error(request, account_or_msg)
    else:
        form = AdminLoginForm()

    return render(request, 'auth/sign-in.html', {'form': form})

def setup_admin(request):
    email = request.GET.get('email', 'admin@travel.com')
    password = request.GET.get('password', 'admin123')

    if Account.objects.filter(email=email).exists():
        return HttpResponse("Admin already exists.")

    Account.objects.create(
        email=email,
        password=make_password(password),
        role='admin'
    )
    return HttpResponse(f"Admin created with email: {email}")

def logout(request):
    request.session.flush()
    return redirect('login')
