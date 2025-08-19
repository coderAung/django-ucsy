import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from travella.dtos.package_search import PublicPackageSearch
from travella.services.package_service import PackageService
from travella.services.package_utils import load_categories, load_locations
from travella.utils.route_view import RouteView

view = RouteView.get('public')

packageService = PackageService()

def discover(request:HttpRequest) -> HttpResponse:
    return render(request, view('discover/index'))

def packages(request:HttpRequest) -> HttpResponse:
    print(PublicPackageSearch.of(request.GET))
    paginationResult = packageService.search_for_customer()
    _list = paginationResult.items
    categories = load_categories()
    locations = load_locations()
    return render(request, view('packages/list'), {
        'list': _list,
        'categories': categories,
        'locations': locations,
        'result': paginationResult,
    })

def package_detail(request:HttpRequest, code:str) -> HttpResponse:
    return render(request, view('packages/detail'))