import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from travella.domains.models.booking_history_model import Refunding
from travella.domains.models.booking_models import Booking
from travella.domains.models.notification_models import CustomerNotification
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


def confirm(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        code = request.POST.get('code', '')
        booking = Booking.objects.get(booking_code = code)
        refunding = Refunding.objects.get(booking = booking)
        refunding.status = Refunding.Status.REFUNDED
        refunding.save()
    
    return redirect('refund_requests')