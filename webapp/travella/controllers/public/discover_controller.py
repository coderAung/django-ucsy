from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from travella.services.package_utils import load_categories, load_locations
from travella.utils.route_view import RouteView

view = RouteView.get('public')

def discover(request:HttpRequest) -> HttpResponse:
    locations = load_locations()
    categories = load_categories()
    return render(request, view('discover/index'), {'locations':locations, 'categories':categories})
