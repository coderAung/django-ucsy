from django.shortcuts import render

from ..domains.models.account_models import Account


def home(request):
    accounts = Account.objects.all()
    return render(request, 'test/home.html', {'list': accounts})

def setting(request):
    return render(request, 'test/setting.html')