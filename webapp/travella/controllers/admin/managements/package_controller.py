from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from ....services.package_service import PackageService
from ....services.package_utils import load_categories

base = 'admin/managements/packages/'

packageService = PackageService()

def view(name: str) -> str:
    return base + name + '.html'

# packages/ GET
def list(request: HttpRequest) -> HttpResponse:
    items = packageService.get_all()
    return render(request, view('list'), {'list': items})

# packages/<id> GET
def detail(request: HttpRequest, code:str) -> HttpResponse:
    dto = packageService.get_one(code)
    return render(request, view('detail'), {'dto': dto})

# packages/new GET
def new(request: HttpRequest) -> HttpResponse:
    categories = load_categories()
    return render(request, view('form'), {'categories': categories})

# packages/save POST
def save(request: HttpRequest) -> HttpResponse:
    return redirect('/admins/packages/')

# packages/<id>/edit/ GET and POST
def edit(request: HttpRequest, id: int) -> HttpResponse:
    return render(request, view('form'))
