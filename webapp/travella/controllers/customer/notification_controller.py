import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from travella.domains.models.booking_history_model import Refunding
from travella.domains.models.notification_models import CustomerNotification
from travella.services import customer_notification_service, payment_request_service
from travella.utils.route_view import RouteView

view = RouteView.get('customer/')

def get_list(request:HttpRequest) -> HttpResponse:
    _list = customer_notification_service.get_list_by_id(request.user.id)
    return render(request, view('notifications'), {
        'list': _list,
    })

def detail(request:HttpRequest, id:uuid) -> HttpResponse:
    noti = customer_notification_service.get_by_id(id)
    if noti.type == CustomerNotification.NotificationType.PAYMENT_RESERVED.value:
        payment = payment_request_service.get_by_id(noti.id)
        return redirect('customer_bookings_detail', id=payment.booking.id)
    if noti.type == CustomerNotification.NotificationType.BOOKING_CANCELLED.value:
        return redirect('refund_detail', id=noti.id)
    if noti.type == CustomerNotification.NotificationType.PAYMENT_REJECTED.value:
        return render(request, view('rejection'), {
            'noti': noti
        })
    
@require_POST
def delete(request:HttpRequest) -> HttpResponse:
    id = request.POST.get('notiId')
    try:
        noti = CustomerNotification.objects.get(id = id)
        noti.image.delete()
        noti.delete()
        return redirect('notifications')
    except ValueError as e:
        return redirect('notifications')
