import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from travella.utils.route_view import RouteView

view = RouteView.get('public')

def discover(request:HttpRequest) -> HttpResponse:
    return render(request, view('discover/index'))

def packages(request:HttpRequest) -> HttpResponse:
    return render(request, view('packages/list'))

def package_detail(request:HttpRequest, code:str) -> HttpResponse:
    return render(request, view('packages/detail'))