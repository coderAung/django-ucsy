from django.db.models import Q, Sum
from travella.domains.models.booking_models import Booking
from travella.dtos.booking_dto import BookingListDTO, BookingDetailDTO
from django.utils import timezone

def calculate_available_tickets(package):
    """Calculate available tickets for a package without modifying the model"""
    booked_count = Booking.objects.filter(
        package=package
    ).exclude(
        status=Booking.Status.CANCELLED
    ).aggregate(
        total=Sum('ticket_count')
    )['total'] or 0
    return max(0, package.total_tickets - booked_count)

def get_all_bookings():
    return Booking.objects.select_related('customer__accountdetail', 'package').all()

def get_booking_by_id(id):
    return Booking.objects.select_related('customer__accountdetail', 'package').get(id=id)

def get_filtered_bookings(query=None, status=None):
    bookings = Booking.objects.select_related('customer__accountdetail', 'package')

    if query:
        bookings = bookings.filter(
            Q(id__icontains=query) |
            Q(customer__email__icontains=query) |
            Q(customer__accountdetail__name__icontains=query)
        )
    
    if status:
        status_map = {
            'pending': Booking.Status.PENDING,
            'reserved': Booking.Status.RESERVED,
            'cancelled': Booking.Status.CANCELLED,
        }
        status_value = status_map.get(status.lower())
        if status_value is not None:
            bookings = bookings.filter(status=status_value)

    return bookings

def get_booking_list_dtos_from_queryset(bookings_queryset):
    dtos = []
    for booking in bookings_queryset:
        customer_name = (
            booking.customer.accountdetail.name
            if hasattr(booking.customer, 'accountdetail') and booking.customer.accountdetail
            else booking.customer.email
        )
        
        # Calculate available tickets
        available_tickets = calculate_available_tickets(booking.package)
        
        # Convert UTC times to local timezone
        created_at_local = timezone.localtime(booking.created_at)
        status_updated_at_local = timezone.localtime(booking.status_updated_at)
        
        dtos.append(BookingListDTO(
            id=booking.id,
            customer_name=customer_name,
            package_title=booking.package.title,
            status_display=booking.get_status_display(),
            created_date=created_at_local.date(),
            created_time=created_at_local.strftime('%I:%M %p').lstrip("0"),
            status_updated_date=status_updated_at_local.date(),
            status_updated_time=status_updated_at_local.strftime('%I:%M %p').lstrip("0"),
            available_tickets=available_tickets,
            total_capacity=booking.package.total_tickets
        ))
    return dtos

def get_booking_detail_dto(booking_id):
    booking = Booking.objects.select_related('customer__accountdetail', 'package').get(id=booking_id)
    account_detail = getattr(booking.customer, 'accountdetail', None)
    
    # Calculate available tickets
    available_tickets = calculate_available_tickets(booking.package)
    
    customer_name = account_detail.name if account_detail else booking.customer.email
    customer_phone = account_detail.phone if account_detail else ''
    
    # Convert UTC times to local timezone
    created_at_local = timezone.localtime(booking.created_at)
    status_updated_at_local = timezone.localtime(booking.status_updated_at)
    
    return BookingDetailDTO(
        id=booking.id,
        status=booking.get_status_display(),
        ticket_count=booking.ticket_count,
        unit_price=float(booking.unitPrice),
        customer_name=customer_name,
        customer_email=booking.customer.email,
        customer_phone=customer_phone,
        package_title=booking.package.title,
        package_departure=booking.package.departure,
        package_duration=booking.package.duration,
        created_date=created_at_local.date(),
        created_time=created_at_local.strftime('%I:%M %p').lstrip("0"),
        status_updated_date=status_updated_at_local.date(),
        status_updated_time=status_updated_at_local.strftime('%I:%M %p').lstrip("0"),
        available_tickets=available_tickets,
        total_capacity=booking.package.total_tickets
    )