from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from travella.services import customer_setting_service
from travella.utils.route_view import RouteView


view = RouteView.get('customer/settings/')

def settings(request:HttpRequest) -> HttpResponse:
    account_info, logs = customer_setting_service.get_setting_dtos(request.user.id)
    return render(request, view('list'), {
        'account_info': account_info,
        'logs': logs,
    })