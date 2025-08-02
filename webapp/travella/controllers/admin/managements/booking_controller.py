from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
from travella.services.booking_service import get_all_bookings, get_booking_by_id


base = 'admin/managements/bookings/'

def view(name: str) -> str:
    return base + name + '.html'

# GET /admins/bookings/
def list(request: HttpRequest) -> HttpResponse:
    bookings = get_all_bookings()
    return render(request, view('list'), {'bookings': bookings})

# GET /admins/bookings/<id>/
def detail(request: HttpRequest, id: int) -> HttpResponse:
    booking = get_booking_by_id(id)
    if booking is None:
        raise Http404("Booking not found")
    
    total_cost = booking.ticketCount * booking.unitPrice
    return render(request, view('detail'), {
        'booking': booking,
        'total_cost': total_cost
    })
