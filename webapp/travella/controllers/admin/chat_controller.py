from dataclasses import dataclass
import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from travella.domains.models.account_models import Account
from travella.utils.route_view import RouteView

view  = RouteView.get('admin')

def chat_list(request:HttpRequest) -> HttpResponse:
    chaters = [Chater(a.id, a.accountdetail.name, a.email) for a in Account.objects.filter(role = Account.Role.CUSTOMER)]
    return render(request, view('chat'), {'chaters': chaters})

def chat_room(request:HttpRequest, id:uuid) -> HttpResponse:
    chaters = [Chater(a.id, a.accountdetail.name, a.email) for a in Account.objects.filter(role = Account.Role.CUSTOMER)]
    customer = Account.objects.get(id=id)
    return render(request, view('chat'), {'chaters': chaters, 'customer': customer})

@dataclass
class Chater:
    id:uuid
    name:str
    email:str