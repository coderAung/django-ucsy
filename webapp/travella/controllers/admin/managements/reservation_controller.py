import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from travella.services import reservation_service
from travella.utils.route_view import RouteView

view = RouteView.get('admin/managements/reservations')

def get_list(request:HttpRequest) -> HttpResponse:
    _list = reservation_service.search_payment_requests()
    return render(request, view('list'), {'list': _list})

def detail(request:HttpRequest, id:uuid) -> HttpResponse:
    payment_request_info, booking_info, package_info = reservation_service.get_dtos(id)
    return render(request, view('detail'), {
        'payment_request_info': payment_request_info,
        'booking_info': booking_info,
        'package_info': package_info,
    })

@require_POST
def save(request:HttpRequest) -> HttpResponse:
    # get id
    id = request.POST.get('reservationId')
    # reserve the request
    try:
        reservation_service.reserve(id, request.user.id)
        # if success => redirect to booking detail with success message
        return redirect('reservations_detail', id=id)
    except:
        return redirect('reservations_detail', id=id)
    # if fail => redirect to payment request detail with error message
    
    pass