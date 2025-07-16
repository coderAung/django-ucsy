from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

base = 'admin/managements/packages/'

def view(name: str) -> str:
    return base + name + '.html'

# packages/ GET
def list(request: HttpRequest) -> HttpResponse:
    return render(request, view('list'))

# packages/<id> GET
def detail(request: HttpRequest, id: int) -> HttpResponse:
    return render(request, view('detail'))

# packages/new GET
def new(request: HttpRequest) -> HttpResponse:
    return render(request, view('form'))

# packages/save POST
def save(request: HttpRequest) -> HttpResponse:
    return redirect('/admins/packages/')

# packages/<id>/edit/ GET and POST
def edit(request: HttpRequest, id: int) -> HttpResponse:
    return render(request, view('form'))
