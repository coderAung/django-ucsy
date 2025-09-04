from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from travella.domains.models.booking_history_model import Refunding
from travella.utils.route_view import RouteView

view = RouteView.get('admin/managements/refunds')

def _list(request:HttpRequest) -> HttpResponse:
    refundings = Refunding.objects.all().order_by('-created_at')
    return render(request, view('list'), {'list': refundings})