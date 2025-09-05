import uuid

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from travella.domains.models.booking_history_model import Refunding
from travella.utils.route_view import RouteView

view = RouteView.get('customer/refund/')

def detail(request:HttpRequest, id:uuid) -> HttpResponse:
    try:
        refund = Refunding.objects.get(id=id)
        return render(request, view('detail'), {
            'refund': refund,
        })
    except ValueError as e:
        messages.error(request, 'Refund Not Found.')
        return redirect('notifications')
    