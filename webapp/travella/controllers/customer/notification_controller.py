from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from travella.services import customer_notification_service
from travella.utils.route_view import RouteView

view = RouteView.get('customer/')

def get_list(request:HttpRequest) -> HttpResponse:
    _list = customer_notification_service.get_list_by_id(request.user.id)
    return render(request, view('notifications'), {
        'list': _list,
    })