from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from travella.utils.route_view import RouteView

base = 'customer/bookings/'
view = RouteView.get(base)

def history(request:HttpRequest) -> HttpResponse:
    return render(request, view('history'))

def detail(request:HttpRequest, id:int) -> HttpResponse:
    return render(request, view('detail'))

def new(request:HttpRequest, code:str) -> HttpResponse:
    return render(request, view('form'))

@require_POST
def save(request:HttpRequest) -> HttpResponse:
    return render('')
