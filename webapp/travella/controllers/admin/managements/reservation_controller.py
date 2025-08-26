import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from travella.services import reservation_service
from travella.utils.route_view import RouteView

view = RouteView.get('admin/managements/reservations')

def get_list(request:HttpRequest) -> HttpResponse:
    _list = reservation_service.search_payment_requests()
    return render(request, view('list'), {'list': _list})

def detail(request:HttpRequest, id:uuid) -> HttpResponse:
    payment_request_info, booking_info, package_info = reservation_service.get_dtos(id)
    return render(request, view('detail'), {
        'payment_request_info': payment_request_info,
        'booking_info': booking_info,
        'package_info': package_info,
    })