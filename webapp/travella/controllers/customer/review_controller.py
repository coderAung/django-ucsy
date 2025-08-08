from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from travella.utils.route_view import RouteView

base = 'customer/reviews/'
view = RouteView.get(base)

def list(request:HttpRequest) -> HttpResponse:
    return render(request, view('list'))

def detail(request:HttpRequest, id:int) -> HttpResponse:
    return render(request, view('detail'))

def new(request:HttpRequest) -> HttpResponse:
    return render(request, view('form'))

def edit(request:HttpRequest, id:int) -> HttpResponse:
    return render(request, view('form'))

@require_POST
def save(request:HttpRequest) -> HttpResponse:
    return render('')

@require_POST
def delete(request:HttpRequest, id:int) -> HttpResponse:
    return render('')