import uuid

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

base = 'admin/managements/users/'

def view(name:str) -> str:
    return base + name + '.html'

# customers/ GET
def list(request:HttpRequest) -> HttpResponse:
    return render(request, view('customer-list'))

# customers/<id:int> GET
def detail(request:HttpRequest, id:uuid) -> HttpResponse:
    return render(request, view('customer-detail'))
