from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from travella.utils.route_view import RouteView


view = RouteView.get('customer/settings/')

def settings(request:HttpRequest) -> HttpResponse:
    return render(request, view('list'))