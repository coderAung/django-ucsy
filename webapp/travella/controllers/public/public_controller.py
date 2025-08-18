import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from travella.services.package_service import PackageService
from travella.services.package_utils import load_categories, load_locations
from travella.utils.route_view import RouteView

view = RouteView.get('public')

packageService = PackageService()

def discover(request:HttpRequest) -> HttpResponse:
    return render(request, view('discover/index'))

def packages(request:HttpRequest) -> HttpResponse:
    _list = packageService.search_for_customer()
    categories = load_categories()
    locations = load_locations()
    return render(request, view('packages/list'), {
        'list': _list,
        'categories': categories,
        'locations': locations
    })

def package_detail(request:HttpRequest, code:str) -> HttpResponse:
    return render(request, view('packages/detail'))