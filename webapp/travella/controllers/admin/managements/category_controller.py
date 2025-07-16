from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

base = 'admin/managements/categories/'

def view(name:str) -> str:
    return base + name + '.html'

# categories/ GET
def list(request:HttpRequest) -> HttpResponse:
    return render(request, view('list'))

# categories/<id> GET
def detail(request:HttpRequest, id:int) -> HttpResponse:
    return render(request, view('detail'))

# categories/new GET
def new(request:HttpRequest) -> HttpResponse:
    return render(request, view('form'))

# categories/save POST
def save(request:HttpRequest) -> HttpResponse:
    return redirect('/admins/categories/')

# categories/<id>/edit/ GET and POST
def edit(request:HttpRequest, id:int) -> HttpResponse:
    return render(request, view('form'))