import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from travella.dtos.package_search import PublicPackageSearch
from travella.services.package_service import PackageService
from travella.services.package_utils import load_categories, load_locations
from travella.utils.route_view import RouteView

view = RouteView.get('public')

packageService = PackageService()

def packages(request:HttpRequest) -> HttpResponse:
    paginationResult = packageService.search_for_customer(PublicPackageSearch.of(request.GET))
    categories = load_categories()
    locations = load_locations()
    return render(request, view('packages/list'), {
        'categories': categories,
        'locations': locations,
        'result': paginationResult,
    })

def package_detail(request:HttpRequest, code:str) -> HttpResponse:
    package_detail = packageService.detail(code = code)
    return render(request, view('packages/detail'), {'dto': package_detail})

def about(request: HttpRequest) -> HttpResponse:

    return render(request, view('about/index'), None)