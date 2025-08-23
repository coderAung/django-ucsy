from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
from travella.domains.models.booking_models import Booking  
from django.utils.timezone import localtime
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
     # Counts for top display
    total_count = Booking.objects.count()
    pending_count = Booking.objects.filter(status=Booking.Status.PENDING).count()
    reserved_count = Booking.objects.filter(status=Booking.Status.RESERVED).count()
    cancelled_count = Booking.objects.filter(status=Booking.Status.CANCELLED).count()

    return render(request, view('list'), {
        'bookings': bookings_dtos,
        'status': status,
        'query': query,
        'total_count': total_count,
        'pending_count': pending_count,
        'reserved_count': reserved_count,
        'cancelled_count': cancelled_count,
    })

def detail(request: HttpRequest, id: str) -> HttpResponse:
    booking = get_booking_by_id(id)
    if booking is None:
        raise Http404("Booking not found")

    total_cost = booking.ticket_count * booking.unit_price

    context = {
        'booking': booking,
        'total_cost': total_cost,
        'pending_date': None,
        'pending_time': None,
        'reserved_or_cancelled_date': None,
        'reserved_or_cancelled_time': None,
        'reserved_by_name': None,
    }

    if booking.status == Booking.Status.PENDING:
        context['pending_date'] = booking.created_at.date()
        context['pending_time'] = booking.created_at.strftime('%I:%M %p').lstrip("0")
        context['reserved_or_cancelled_date'] = "-"
        context['reserved_or_cancelled_time'] = "-"

    elif booking.status == Booking.Status.RESERVED:
        context['reserved_or_cancelled_date'] = booking.status_updated_at.date()
        context['reserved_or_cancelled_time'] = booking.status_updated_at.strftime('%I:%M %p').lstrip("0")
        try:
            context['reserved_by_name'] = booking.history.reservedBy.accountdetail.name
        except Exception:
            context['reserved_by_name'] = "-"

    elif booking.status == Booking.Status.CANCELLED:
        context['reserved_or_cancelled_date'] = booking.status_updated_at.date()
        context['reserved_or_cancelled_time'] = booking.status_updated_at.strftime('%I:%M %p').lstrip("0")

    return render(request, view('detail'), context)
