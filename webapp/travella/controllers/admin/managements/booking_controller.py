from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
from travella.dtos.booking_dto import BookingFilterDTO
from travella.services.booking_service import (
    get_booking_by_id,
    get_filtered_bookings,
    get_all_bookings,
    get_booking_list_dtos_from_queryset,
)

base = 'admin/managements/bookings/'

def view(name: str) -> str:
    return base + name + '.html'

# GET /admins/bookings/
def list(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("query", "").strip()
    status = request.GET.get("status", "").strip()

    if query or status:
        bookings_qs = get_filtered_bookings(query=query, status=status)
    else:
        bookings_qs = get_all_bookings()

    bookings_dtos = get_booking_list_dtos_from_queryset(bookings_qs)
    return render(request, view('list'), {
        'bookings': bookings_dtos,
        'status': status,
        'query': query,
    })

# GET /admins/bookings/<id>/
def detail(request: HttpRequest, id: str) -> HttpResponse:
    booking = get_booking_by_id(id)
    if booking is None:
        raise Http404("Booking not found")

    total_cost = booking.ticketCount * booking.unitPrice
    return render(request, view('detail'), {
        'booking': booking,
        'total_cost': total_cost,
    })
