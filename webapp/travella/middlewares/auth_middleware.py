from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.conf import settings

from travella.domains.models.account_models import Account


class AuthMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        self.admin_urls = []
        self.customer_urls = []
        self.auth_urls = []
        self.public_urls = [
            '/auth/sign-in',
            '/auth/sign-up',
            '/public',
            '/media/public',
            '/test/'
        ]
    
    def __call__(self, request:HttpRequest) -> HttpResponse:
        path = request.path_info
        if request.path == '/':
            return redirect('/public/discover')
        if not request.user.is_authenticated and not any(path.startswith(url) for url in self.public_urls):
            return redirect(f'{settings.LOGIN_URL}?next={request.path}')
        if request.user.is_authenticated:
            user = request.user
            if user.role == Account.Role.CUSTOMER and path.startswith('/admins/'):
                return redirect('/authorization/fail')
            if (user.role == Account.Role.ADMIN or user.role == Account.Role.MOD) and path.startswith('/customer/'):
                return redirect('/authorization/fail')
        return self.get_response(request)