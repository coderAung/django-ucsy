import uuid
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from travella.dtos.package_dto import PackageItem
from travella.dtos.api_dtos import BookingOverview

from ....services.package_service import PackageService
from ....services.package_utils import is_empty, load_categories, load_status

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
    items = packageService.search(request.GET)
    categories = load_categories()
    status = load_status()
    return render(request, view('list'), {'list': items, 'categories': categories, 'status': status})

# packages/<id> GET
def detail(request: HttpRequest, code:str) -> HttpResponse:
    dto = packageService.get_one(code)
    return render(request, view('detail'), {'dto': dto})

# packages/new GET
def new(request: HttpRequest) -> HttpResponse:
    categories = load_categories()
    return render(request, view('form'), {'categories': categories})

# packages/save POST
@require_POST
def save(request: HttpRequest) -> HttpResponse:
    code = request.POST.get('code')
    name = request.POST.get('name')
    print(f'code : {code}\nname : {name}')
    images = request.FILES.getlist('images[]')
    for i in images:
        print(f'file : {i.name}')
    return redirect('/admins/packages/')

# packages/<id>/edit/ GET and POST
def edit(request: HttpRequest, id: int) -> HttpResponse:
    return render(request, view('form'))
