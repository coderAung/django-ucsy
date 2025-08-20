import uuid

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

base = 'admin/managements/users/'

def view(name:str) -> str:
    return base + name + '.html'

# staffs/ GET
def list(request:HttpRequest) -> HttpResponse:
    return render(request, view('staff-list'))

def detail(request:HttpRequest, id:uuid) -> HttpResponse:
    return render(request, view('staff-detail'))