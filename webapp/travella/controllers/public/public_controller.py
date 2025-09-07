import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from travella.domains.models.chat_message_models import ChatMessage
from travella.domains.models.limit_models import AccountLimit
from travella.dtos.package_search import PublicPackageSearch
from travella.services import account_limit_service, itinerary_service
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
    itineraries = itinerary_service.get_by_package_code(code)
    return render(request, view('packages/detail'), {
        'dto': package_detail,
        'itineraries': itineraries,
    })

def about(request: HttpRequest) -> HttpResponse:
    return render(request, view('about/index'), None)

def help_support(request):
    return render(request, 'support/help.html')

def contact_us(request:HttpRequest):
    if(request.user.is_authenticated):
        chat_messages = ChatMessage.objects.filter(customer__id=request.user.id)
        chat_limit = account_limit_service.get_limit_counts(request.user.id, AccountLimit.Type.CHAT)
        return render(request, 'contact_us/chat-us.html', {'chat_messages': chat_messages, 'chat_limit': chat_limit})
    return render(request, 'contact_us/chat-us.html')
