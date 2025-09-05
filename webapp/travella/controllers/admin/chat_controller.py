from dataclasses import dataclass
import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.db.models import Count, Q, Max, F

from travella.domains.models.account_models import Account
from travella.domains.models.chat_message_models import ChatMessage
from travella.utils.route_view import RouteView

view  = RouteView.get('admin')

def _build_chaters_qs():
    return (
        Account.objects.filter(role=Account.Role.CUSTOMER)
        .annotate(
            # last message in the thread with this customer (any direction)
            last_message_time=Max("customer_messages__created_at"),
            # unread = messages sent BY the customer that haven't been read yet
            unread_count=Count(
                "customer_messages",
                filter=Q(
                    customer_messages__is_read=False,
                    customer_messages__sender_id=F("id"),
                ),
            ),
        )
        .order_by("-last_message_time", "accountdetail__name")
    )

def chat_list(request:HttpRequest) -> HttpResponse:

    customers = _build_chaters_qs()
    chaters = [Chater(a.id, a.accountdetail.name, a.email, a.accountdetail.photo.url if a.accountdetail.photo else '', a.unread_count) for a in customers]

    return render(request, view('chat'), {'chaters': chaters})

def chat_room(request:HttpRequest, id:uuid) -> HttpResponse:
    customer = Account.objects.get(id=id)
    ChatMessage.objects.filter(customer__id=customer.id, is_read=False).update(is_read=True)
    customers = _build_chaters_qs()
    chaters = [Chater(a.id, a.accountdetail.name, a.email, a.accountdetail.photo.url if a.accountdetail.photo else '', a.unread_count) for a in customers]
    chat_messages = ChatMessage.objects.filter(customer__id=customer.id)
    return render(request, view('chat'), {'chaters': chaters, 'customer': customer, 'chat_messages': chat_messages,})

@dataclass
class Chater:
    id:uuid
    name:str
    email:str
    photo:str
    unread_count:int = 0