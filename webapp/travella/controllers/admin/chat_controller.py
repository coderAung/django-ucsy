from dataclasses import dataclass
import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from travella.domains.models.account_models import Account
from travella.domains.models.chat_message_models import ChatMessage
from travella.utils.route_view import RouteView

view  = RouteView.get('admin')

def chat_list(request:HttpRequest) -> HttpResponse:
    chaters = [Chater(a.id, a.accountdetail.name, a.email, a.accountdetail.photo.url if a.accountdetail.photo else '') for a in Account.objects.filter(role = Account.Role.CUSTOMER)]
    return render(request, view('chat'), {'chaters': chaters})

def chat_room(request:HttpRequest, id:uuid) -> HttpResponse:
    chaters = [Chater(a.id, a.accountdetail.name, a.email, a.accountdetail.photo.url if a.accountdetail.photo else '') for a in Account.objects.filter(role = Account.Role.CUSTOMER)]
    customer = Account.objects.get(id=id)
    chat_messages = ChatMessage.objects.filter(customer__id=customer.id)
    return render(request, view('chat'), {'chaters': chaters, 'customer': customer, 'chat_messages': chat_messages,})

@dataclass
class Chater:
    id:uuid
    name:str
    email:str
    photo:str