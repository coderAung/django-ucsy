import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from travella.services import booking_auto_service


@require_POST
def cancel_booking(request:HttpRequest, id:uuid) -> HttpResponse:
    if booking_auto_service.is_refundable(id):
        print('============== Refundable booking cancellation ==============')
        return cancel_refundable_booking(request, id)
    else:
        booking_auto_service.cancel_booking(id)
        messages.success(request, 'Booking is cancelled successfully.')
    return redirect('customer_bookings_detail', id=id)

def cancel_refundable_booking(request:HttpRequest, id:uuid) -> HttpResponse:
    form = booking_auto_service.RefundForm(id, request)
    booking_auto_service.cancel_refundable_booking(form)
    messages.success(request, 'Booking is cancelled. Refunding is processing.')
    return redirect('customer_bookings_detail', id=id)