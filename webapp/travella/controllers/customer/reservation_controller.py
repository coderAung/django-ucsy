from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from travella.utils.route_view import RouteView

base = 'customer/reservations'
view = RouteView.get(base)

def save(request:HttpRequest) -> HttpResponse:
    return render(request, '')

def history(request:HttpRequest) -> HttpResponse:
    return render(request, view('history'))

def voucher(request:HttpRequest, id:int) -> HttpResponse:
    return render(request, view('voucher'))