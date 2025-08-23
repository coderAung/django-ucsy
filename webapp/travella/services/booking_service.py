from travella.domains.models.booking_models import Booking
from travella.dtos.booking_dto import BookingListDTO, BookingDetailDTO, BookingFilterDTO
from django.db.models import Q


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
        # Map status string to Booking.Status integer
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
    for b in bookings_queryset:
        customer_name = (
            b.customer.accountdetail.name
            if hasattr(b.customer, 'accountdetail')
            else b.customer.email
        )
        dtos.append(BookingListDTO(
            id=b.id,
            customer_name=customer_name,
            package_title=b.package.title,
            status_display=b.get_status_display(),
            created_date=b.created_at.date(),
            created_time=b.created_at.strftime('%I:%M %p').lstrip("0"),
            status_updated_date=b.status_updated_at.date(),
            status_updated_time=b.status_updated_at.strftime('%I:%M %p').lstrip("0"),
        ))
    return dtos





def get_booking_detail_dto(booking_id):
    b = Booking.objects.select_related('customer__accountdetail', 'package').get(id=booking_id)
    account_detail = getattr(b.customer, 'accountdetail', None)
    
    customer_name = account_detail.name if account_detail else b.customer.email
    customer_phone = account_detail.phone if account_detail else ''
    
    return BookingDetailDTO(
        id=b.id,
        status=b.get_status_display(),
        ticket_count=b.ticket_count,
        unit_price=b.unit_price,
        customer_name=customer_name,
        customer_email=b.customer.email,
        customer_phone=customer_phone,
        package_title=b.package.title,
        package_departure=b.package.departure,
        package_duration=b.package.duration,
    )

