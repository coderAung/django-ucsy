from django.shortcuts import render

from travella.domains.models.log_models import AccessLog
from travella.domains.models.payment_models import PaymentRequest
from travella.domains.models.tour_models import PackageData
from travella.tests.tests import load_package_data

from ..domains.models.account_models import Account


def home(request):
    accounts = Account.objects.all()
    return render(request, 'test/home.html', {'list': accounts})

def setting(request):
    load_package_data()
    logs = AccessLog.objects.all()
    return render(request, 'test/setting.html', {'datas': PackageData.objects.all(), 'logs': logs})

def pay(request):
    data = PaymentRequest.objects.all()
    return render(request, 'test/pay.html', {'data': data})