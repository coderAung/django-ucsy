import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.contrib import messages

from travella.dtos.reservation_search import ReservationSearch
from travella.services import reservation_service
from travella.services.package_utils import is_empty
from travella.utils.route_view import RouteView

view = RouteView.get('admin/managements/reservations')

def get_list(request:HttpRequest) -> HttpResponse:
    search = ReservationSearch(request.GET)
    page = 1
    if not is_empty(request.GET.get('page')):
        page = int(request.GET.get('page'))
    pagination_result = reservation_service.search_payment_requests(search, int(page)) 
    _list = pagination_result.items
    return render(request, view('list'), {
        'list': _list,
        'result': pagination_result,
        })

def detail(request:HttpRequest, id:uuid) -> HttpResponse:
    payment_request_info, booking_info, package_info = reservation_service.get_dtos(id)
    if payment_request_info.is_reserved:
        reserved_by_account = reservation_service.get_reserver(payment_request_info.reservation_id)
        return render(request, view('detail'), {
        'payment_request_info': payment_request_info,
        'booking_info': booking_info,
        'package_info': package_info,
        'reserver': reserved_by_account,
        })
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
        messages.success(request, 'Booking is successfully reserved.')
        return redirect('reservations_detail', id=id)
    except:
        # if fail => redirect to payment request detail with error message
        return redirect('reservations_detail', id=id)
