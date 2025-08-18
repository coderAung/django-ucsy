from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
from travella.domains.models.booking_models import Booking  
from travella.domains.models.account_models import AccountDetail
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

def list(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("query", "").strip()
    status = request.GET.get("status", "").strip()

    if query or status:
        bookings_qs = get_filtered_bookings(query=query, status=status)
    else:
        bookings_qs = get_all_bookings()

    bookings_dtos = get_booking_list_dtos_from_queryset(bookings_qs)
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

    total_cost = booking.ticketCount * booking.unitPrice

    # Get customer details with fallbacks
    try:
        account_detail = AccountDetail.objects.get(account=booking.customer)
        customer_name = account_detail.name
        customer_phone = account_detail.phone
    except AccountDetail.DoesNotExist:
        customer_name = booking.customer.email
        customer_phone = "Not provided"

    # Initialize context with basic info
    context = {
        'booking': booking,
        'total_cost': total_cost,
        'customer_name': customer_name,
        'customer_email': booking.customer.email,
        'customer_phone': customer_phone,
        'pending_date': booking.createdAt.date(),
        'pending_time': booking.createdAt.strftime('%I:%M %p').lstrip("0"),
        'reserved_or_cancelled_date': None,
        'reserved_or_cancelled_time': None,
        'reserved_by_name': None,
    }

    # Handle status-specific information
    if booking.status == Booking.Status.PENDING:
        context['reserved_or_cancelled_date'] = "-"
        context['reserved_or_cancelled_time'] = "-"

    elif booking.status in [Booking.Status.RESERVED, Booking.Status.CANCELLED]:
        context['reserved_or_cancelled_date'] = booking.statusUpdatedAt.date()
        context['reserved_or_cancelled_time'] = booking.statusUpdatedAt.strftime('%I:%M %p').lstrip("0")

        if booking.status == Booking.Status.RESERVED:
            try:
                # Try to get admin name from account detail first
                context['reserved_by_name'] = booking.history.reservedBy.accountdetail.name
            except AttributeError:
                try:
                    # Fallback to admin email if name doesn't exist
                    context['reserved_by_name'] = booking.history.reservedBy.email
                except AttributeError:
                    # Final fallback if history is missing
                    context['reserved_by_name'] = "Unknown admin"

    return render(request, view('detail'), context)