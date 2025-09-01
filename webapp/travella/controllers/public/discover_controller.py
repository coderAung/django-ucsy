from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from travella.services.discover_service import get_discover_data
from travella.services.package_utils import load_categories, load_locations
from travella.utils.route_view import RouteView
from travella.services.package_service import PackageService

view = RouteView.get('public')

def discover(request: HttpRequest) -> HttpResponse:
    # Fetch stats and other data
    stats = get_discover_data()
    locations = load_locations()
    categories = load_categories()
    most_booked_packages = PackageService().get_most_booked_packages(count=3)
    print(most_booked_packages)

    context = {
        **stats,
        'locations': locations,
        'categories': categories,
        'most_booked_packages': most_booked_packages,
    }

    return render(request, view('discover/index'), context)
