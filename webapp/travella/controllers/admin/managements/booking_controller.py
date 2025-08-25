from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from travella.domains.models.booking_models import Booking  
from travella.domains.models.account_models import AccountDetail
from travella.domains.models.booking_history import Reservation
from travella.services.booking_service import (
    get_booking_by_id,
    get_filtered_bookings,
    get_all_bookings,
    get_booking_list_dtos_from_queryset,  # This uses calculate_available_tickets internally
)

base = 'admin/managements/bookings/'

def view(name: str) -> str:
    return base + name + '.html'

def list(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("query", "").strip()
    status = request.GET.get("status", "").strip()
    page_number = request.GET.get('page', 1)

    if query or status:
        bookings_qs = get_filtered_bookings(query=query, status=status)
    else:
        bookings_qs = get_all_bookings()

    # Create paginator - 20 items per page
    paginator = Paginator(bookings_qs, 20)
    page_obj = paginator.get_page(page_number)
    
    # This function internally uses calculate_available_tickets
    bookings_dtos = get_booking_list_dtos_from_queryset(page_obj.object_list)
    
    # Get counts for each status
    status_counts = Booking.objects.aggregate(
        total=Count('id'),
        pending=Count('id', filter=Q(status=Booking.Status.PENDING)),
        reserved=Count('id', filter=Q(status=Booking.Status.RESERVED)),
        cancelled=Count('id', filter=Q(status=Booking.Status.CANCELLED)),
    )

    # Prepare pagination context
    pagination_context = {
        'has_prev': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'prev_page': page_obj.previous_page_number() if page_obj.has_previous() else 1,
        'next_page': page_obj.next_page_number() if page_obj.has_next() else paginator.num_pages,
        'current_page': page_obj.number,
        'pages': paginator.page_range,
    }

    return render(request, view('list'), {
        'bookings': bookings_dtos,
        'result': pagination_context,
        'status': status,
        'query': query,
        'total_count': status_counts['total'],
        'pending_count': status_counts['pending'],
        'reserved_count': status_counts['reserved'],
        'cancelled_count': status_counts['cancelled'],
        'page_obj': page_obj,
    })

def detail(request: HttpRequest, id: str) -> HttpResponse:
    booking = get_booking_by_id(id)
    if booking is None:
        raise Http404("Booking not found")

    total_cost = booking.ticket_count * booking.unit_price

    # Get customer details with fallbacks
    try:
        account_detail = AccountDetail.objects.get(account=booking.customer)
        customer_name = account_detail.name
        customer_phone = account_detail.phone
    except AccountDetail.DoesNotExist:
        customer_name = booking.customer.email
        customer_phone = "Not provided"

    # Get reservation history with fallback to admin email
    reserved_by_name = None
    if booking.status == Booking.Status.RESERVED:
        try:
            history = Reservation.objects.get(booking=booking)
            try:
                reserved_by_name = history.reservedBy.accountdetail.name
            except AttributeError:
                reserved_by_name = history.reservedBy.email  # Fallback to email
        except Reservation.DoesNotExist:
            reserved_by_name = "Unknown admin"

    # Convert UTC times to local timezone
    created_at_local = timezone.localtime(booking.created_at)
    status_updated_at_local = timezone.localtime(booking.status_updated_at) if booking.status != Booking.Status.PENDING else None

    # Initialize context with basic info
    context = {
        'booking': booking,
        'total_cost': total_cost,
        'customer_name': customer_name,
        'customer_email': booking.customer.email,
        'customer_phone': customer_phone,
        'pending_date': created_at_local.date(),
        'pending_time': created_at_local.strftime('%I:%M %p').lstrip("0"),
        'reserved_or_cancelled_date': status_updated_at_local.date() if status_updated_at_local else "-",
        'reserved_or_cancelled_time': status_updated_at_local.strftime('%I:%M %p').lstrip("0") if status_updated_at_local else "-",
        'reserved_by_name': reserved_by_name,
    }

    return render(request, view('detail'), context)
