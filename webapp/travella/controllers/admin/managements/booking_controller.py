from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

base = 'admin/managements/bookings/'

def view(name:str) -> str:
    return base + name + '.html'

# bookings/ GET
def list(request:HttpRequest) -> HttpResponse:
    return render(request, view('list'))

# bookings/<id> GET
def detail(request:HttpRequest, id:int) -> HttpResponse:
    return render(request, view('detail'))
