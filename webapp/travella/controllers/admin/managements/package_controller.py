import uuid
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Sum
from travella.domains.models.booking_models import Booking
from travella.domains.models.tour_models import Package
from travella.dtos.itinerary_forms import ItineraryForm
from travella.dtos.package_dto import PackageItem
from travella.dtos.api_dtos import BookingOverview
from travella.dtos.package_form import PackageForm
from travella.domains.models.tour_models import Package, Category  
from travella.dtos.package_search import PackageSearch
from travella.services import itinerary_service
from travella.services.auth_user import get_auth_user
from travella.tests.tests import load_package_data




from ....services.package_service import PackageService
from ....services.package_utils import is_empty, load_categories, load_locations, load_status
from travella.services import package_service

base = 'admin/managements/packages/'

packageService = PackageService()

def view(name: str) -> str:
    return base + name + '.html'


@require_GET
def booking_overview(requset:HttpRequest, id:uuid) -> JsonResponse:
    overview:BookingOverview = packageService.booking_overview(id)
    return JsonResponse(overview.json())

# packages/ GET
def list(request: HttpRequest) -> HttpResponse:
    load_package_data()

    result = packageService.search_list(PackageSearch(request))
    # items = packageService.search(request.GET)
    items = result.items
    categories = load_categories()
    status = load_status()
    return render(request, view('list'), {'list': items, 'categories': categories, 'status': status, 'result': result})

# packages/<id> GET
def detail(request: HttpRequest, code:str) -> HttpResponse:
    dto = packageService.get_one(code)
    gallery = packageService.get_gallery(code)
    return render(request, view('detail'), {'dto': dto, 'gallery': gallery})

# packages/new GET
def new(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        return save(request)
    categories = load_categories()
    transportations = [t for t in Package.Transportation]
    locations = load_locations()
    return render(request, view('form'), {
        'categories': categories,
        'transportations': transportations,
        'locations': locations})

# packages/save POST
def save(request: HttpRequest) -> HttpResponse:
    form, errors = PackageForm.of(request.POST)
    if len(errors) > 0:
        print(errors)
        categories = load_categories()
        return render(request, view('form'), {'categories': categories})

    images = request.FILES.getlist('images[]')
    code:str = packageService.save(get_auth_user(request), form, images)
    return redirect('edit_itinerary', code = code)

# packages/<id>/edit/ GET and POST
def edit(request: HttpRequest, code: str) -> HttpResponse:
    return render(request, view('form'))

def edit_itinerary(request: HttpRequest, code: str) -> HttpResponse:
    if request.method == 'POST':
        return save_itinerary(request, code)
    _list = itinerary_service.get_by_package_code(code)
    duration = package_service.duration_by_code(code)
    days = [i+1 for i in range(duration)]
    if _list:
        days = [d for d in days if d not in [i.day for i in _list]]
    
    return render(request, view('itinerary-form'), {
        'list': _list,
        'days': days,
        'code': code,
    })

def save_itinerary(request: HttpRequest, code:str) -> HttpResponse:
    form = ItineraryForm(request)
    itinerary_service.save(form=form, package_code=code)
    return redirect('edit_itinerary', code=code)


@require_POST
def delete(request: HttpRequest) -> HttpResponse:
    code = request.POST.get('code')
    packageService.delete(code)
    return redirect('packages')
