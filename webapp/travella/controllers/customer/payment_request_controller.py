import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from travella.dtos.reservation_dtos import PaymentRequestForm
from travella.exceptions.business_exception import BusinessException
from travella.services import payment_request_service
from travella.services.payment_request_service import load_payments
from travella.utils.route_view import RouteView

base = 'customer/reservations'
view = RouteView.get(base)

def new(request:HttpRequest, id:uuid) -> HttpResponse:
    if not payment_request_service.is_authorize(id, request.user.id):
        return redirect('/authorization/fail')

    if request.method == 'POST':
        return save(request)
    try:
        package_info, booking_info = payment_request_service.get_reservation_dtos(id, request.user.id)
        payments = load_payments()
        return render(request, view('form'), {
            'payments': payments,
            'package_info': package_info,
            'booking_info': booking_info,
            })
    except BusinessException as e:
        messages.error(request, e.get_message())
        return redirect('customer_bookings_detail', id=id)


def save(request:HttpRequest) -> HttpResponse:
    form = PaymentRequestForm.of(request.POST, request.FILES)
    customer_id = request.user.id
    payment_request_service.save(customer_id, form)
    return redirect('pay')

def history(request:HttpRequest) -> HttpResponse:
    return render(request, view('history'))

def voucher(request:HttpRequest, id:int) -> HttpResponse:
    return render(request, view('voucher'))