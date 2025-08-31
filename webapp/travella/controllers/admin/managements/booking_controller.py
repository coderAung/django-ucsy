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

    # SORT BY LATEST BOOKINGS FIRST - ADD THIS LINE
    bookings_qs = bookings_qs.order_by('-created_at')

    # Create paginator - 20 items per page
    paginator = Paginator(bookings_qs, 20)
    page_obj = paginator.get_page(page_number)
    
    # This function internally uses calculate_available_tickets
    bookings_dtos = get_booking_list_dtos_from_queryset(page_obj.object_list)
    
    # Get counts for each status - ADDED REQUESTING COUNT
    status_counts = Booking.objects.aggregate(
        total=Count('id'),
        pending=Count('id', filter=Q(status=Booking.Status.PENDING)),
        reserved=Count('id', filter=Q(status=Booking.Status.RESERVED)),
        cancelled=Count('id', filter=Q(status=Booking.Status.CANCELLED)),
        requesting=Count('id', filter=Q(status=Booking.Status.REQUESTING)),
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
        'requesting_count': status_counts['requesting'],
        'page_obj': page_obj,
    })
def detail(request: HttpRequest, id: str) -> HttpResponse:
    booking_obj = get_booking_by_id(id)  # Renamed to avoid conflict
    if booking_obj is None:
        raise Http404("Booking not found")

    total_cost = booking_obj.ticket_count * booking_obj.unit_price

    # Get customer details with fallbacks
    try:
        account_detail = AccountDetail.objects.get(account=booking_obj.customer)
        customer_name = account_detail.name
        customer_phone = account_detail.phone
    except AccountDetail.DoesNotExist:
        customer_name = booking_obj.customer.email
        customer_phone = "Not provided"

    # Get reservation history with fallback to admin email
    reserved_by_name = None
    if booking_obj.status == Booking.Status.RESERVED:
        try:
            history = Reservation.objects.get(booking=booking_obj)
            try:
                reserved_by_name = history.reservedBy.accountdetail.name
            except AttributeError:
                reserved_by_name = history.reservedBy.email  # Fallback to email
        except Reservation.DoesNotExist:
            reserved_by_name = "Unknown admin"

    # Convert UTC times to local timezone
    created_at_local = timezone.localtime(booking_obj.created_at)
    status_updated_at_local = timezone.localtime(booking_obj.status_updated_at) if booking_obj.status_updated_at else None

    # Handle different statuses for date/time display
    if booking_obj.status == Booking.Status.PENDING:
        # For Pending, show created date/time
        status_date = created_at_local.date()
        status_time = created_at_local.strftime('%I:%M %p').lstrip("0")
        status_date_label = "Pending Date"
        status_time_label = "Pending Time"
    elif booking_obj.status == Booking.Status.REQUESTING:
        # For Requesting, show status updated date/time (when payment was requested)
        status_date = status_updated_at_local.date() if status_updated_at_local else created_at_local.date()
        status_time = status_updated_at_local.strftime('%I:%M %p').lstrip("0") if status_updated_at_local else created_at_local.strftime('%I:%M %p').lstrip("0")
        status_date_label = "Requested Date"
        status_time_label = "Requested Time"
    else:
        # For Reserved and Cancelled, show status updated date/time
        status_date = status_updated_at_local.date() if status_updated_at_local else "-"
        status_time = status_updated_at_local.strftime('%I:%M %p').lstrip("0") if status_updated_at_local else "-"
        status_date_label = "Reserved Date" if booking_obj.status == Booking.Status.RESERVED else "Cancelled Date"
        status_time_label = "Reserved Time" if booking_obj.status == Booking.Status.RESERVED else "Cancelled Time"

    # Initialize context with basic info
    context = {
        'booking': booking_obj,  # Pass the booking object to template
        'total_cost': total_cost,
        'customer_name': customer_name,
        'customer_email': booking_obj.customer.email,
        'customer_phone': customer_phone,
        'created_date': created_at_local.date(),
        'created_time': created_at_local.strftime('%I:%M %p').lstrip("0"),
        'status_date': status_date,
        'status_time': status_time,
        'status_date_label': status_date_label,
        'status_time_label': status_time_label,
        'reserved_by_name': reserved_by_name,
        'booking_status': booking_obj.status,  # Add raw status for template logic
    }

    return render(request, view('detail'), context)