import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from travella.utils.route_view import RouteView

base = 'customer/reservations'
view = RouteView.get(base)

def new(request:HttpRequest, id:uuid) -> HttpResponse:
    if request.method == 'POST':
        pass
    return render(request, view('form'))

def history(request:HttpRequest) -> HttpResponse:
    return render(request, view('history'))

def voucher(request:HttpRequest, id:int) -> HttpResponse:
    return render(request, view('voucher'))