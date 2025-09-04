import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from travella.domains.models.booking_history_model import Refunding
from travella.utils.route_view import RouteView

view = RouteView.get('admin/managements/refunds')

def get_list(request:HttpRequest) -> HttpResponse:
    refundings = Refunding.objects.all().order_by('-created_at')
    return render(request, view('list'), {'list': refundings})

def detail(request:HttpRequest, id:uuid) -> HttpResponse:
    try:
        dto = Refunding.objects.get(id=id)
        return render(request, view('detail'), {'refund': dto})        
    except ValueError as e:
        redirect('refund_requests')
