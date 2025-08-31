from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import timedelta
from travella.domains.models.tour_models import Package, PackageData
from travella.domains.models.booking_models import Booking
from travella.domains.models.account_models import AccountDetail

# Import the function from your admin service
from travella.services.booking_service import calculate_available_tickets

BASE_TEMPLATE_PATH = 'customer/bookings/'

@login_required
def new(request, code: str):
    """Display the booking form for a package."""
    package = get_object_or_404(Package, code=code)

    if package.data.status != PackageData.Status.AVAILABLE:
        messages.error(request, "This tour is no longer available for booking.")
        return redirect('customer_booking_history')

    # Get user account details for auto-filling the form
    try:
        account_detail = AccountDetail.objects.get(account=request.user)
        user_name = account_detail.name
        user_phone = account_detail.phone
    except AccountDetail.DoesNotExist:
        user_name = request.user.email
        user_phone = ""

    # Use the imported function to calculate available seats
    available_seats = calculate_available_tickets(package)
    
    # Calculate tour end date (departure date + duration)
    tour_end_date = None
    if package.departure and package.duration:
        tour_end_date = package.departure + timedelta(days=package.duration)

    context = {
        'package': package,
        'price_per_seat': f"{package.price:.2f} MMK",
        'price_per_seat_value': float(package.price),
        'departure_date': package.departure.strftime("%B %d, %Y") if package.departure else "N/A",
        'tour_end_date': tour_end_date.strftime("%B %d, %Y") if tour_end_date else "N/A",
        'user_name': user_name,
        'user_email': request.user.email,
        'user_phone': user_phone,
        'available_seats': available_seats,
    }
    return render(request, BASE_TEMPLATE_PATH + 'form.html', context)

@login_required
def history(request):
    bookings = Booking.objects.filter(customer=request.user) \
        .select_related('package', 'customer').order_by('-created_at')

    status_labels = dict(Booking.Status.choices)
    status_classes = {
        Booking.Status.PENDING: "badge-blue",     
        Booking.Status.RESERVED: "badge-green",    
        Booking.Status.CANCELLED: "badge-red",      
        Booking.Status.REQUESTING: "badge-purple",   
    }

    for booking in bookings:
        try:
            customer_name = booking.customer.accountdetail.name
        except AttributeError:
            customer_name = booking.customer.email
        booking.customer_name = customer_name

        booking.status_class = status_classes.get(booking.status, "badge-gray")
        booking.status_label = status_labels.get(booking.status, "Unknown")
        booking.total_price = booking.ticket_count * booking.unit_price 

    return render(request, 'customer/bookings/history.html', {
        "bookings": bookings,
    })



@login_required
def detail(request, id):
    """Show details for a specific booking."""
    booking = get_object_or_404(Booking, id=id, customer=request.user)

    # Total cost
    booking.total_price = booking.ticket_count * booking.unit_price

    # Tour end date
    tour_end_date = None
    if booking.package.departure and booking.package.duration:
        tour_end_date = booking.package.departure + timedelta(days=booking.package.duration)

    # Customer name
    try:
        booking.customer_name = booking.customer.accountdetail.name
    except AttributeError:
        booking.customer_name = booking.customer.email

    # Status label & badge class
    status_labels = dict(Booking.Status.choices)
    status_classes = {
        Booking.Status.PENDING: "badge-blue",
        Booking.Status.RESERVED: "badge-green",
        Booking.Status.CANCELLED: "badge-red",
        Booking.Status.REQUESTING: "badge-purple",
    }
    booking.status_label = status_labels.get(booking.status, "Unknown")
    booking.status_class = status_classes.get(booking.status, "badge-gray")

    # Transportation (default if not set)
    booking.package.transportation = getattr(booking.package, 'transportation', 'N/A')

    return render(request, BASE_TEMPLATE_PATH + 'detail.html', {
        "booking": booking,
        "tour_end_date": tour_end_date.strftime("%B %d, %Y") if tour_end_date else "N/A",
    })

@require_POST
@login_required
def save(request):
    """Save a new booking ONLY when user confirms in the modal."""
    try:
        # Get form data
        package_id = request.POST.get('package_id')
        ticket_count = int(request.POST.get('ticket_count', 1))
        full_name = request.POST.get('fullName', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        # Validate required fields
        if not all([package_id, ticket_count, full_name, email, phone]):
            return JsonResponse({'error': 'All fields are required'}, status=400)

        package = get_object_or_404(Package, id=package_id)

        # Use the imported function to check availability
        available_tickets = calculate_available_tickets(package)
        
        if ticket_count > available_tickets:
            return JsonResponse({
                'error': f'Only {available_tickets} ticket(s) available. You requested {ticket_count}.'
            }, status=400)

        # Create booking
        booking = Booking.objects.create(
            package=package,
            customer=request.user,
            ticket_count=ticket_count,
            unit_price=Decimal(str(package.price)),
            status=Booking.Status.PENDING
        )

        # Update user's account details
        AccountDetail.objects.update_or_create(
            account=request.user,
            defaults={
                'name': full_name,
                'phone': phone
            }
        )

        return JsonResponse({
            'success': True,
            'booking_id': str(booking.id),
            'booking_date': booking.created_at.isoformat(),
            'booking_time': booking.created_at.strftime('%I:%M %p').lstrip("0"),
            'message': 'Booking created successfully'
        })

    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)