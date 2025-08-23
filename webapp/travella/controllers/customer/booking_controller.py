from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
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

    context = {
        'package': package,
        'price_per_seat': f"{package.price:.2f} MMK",
        'price_per_seat_value': float(package.price),
        'departure_date': package.departure.strftime("%B %d, %Y") if package.departure else "N/A",
        'user_name': user_name,
        'user_email': request.user.email,
        'user_phone': user_phone,
        'available_seats': available_seats,
    }
    return render(request, BASE_TEMPLATE_PATH + 'form.html', context)

@login_required
def history(request):
    """Show all bookings for the current user."""
    bookings = Booking.objects.filter(customer=request.user).select_related('package').order_by('-created_at')
    return render(request, BASE_TEMPLATE_PATH + 'history.html', {
        "bookings": bookings,
        "status_labels": dict(Booking.Status.choices)
    })

@login_required
def detail(request, id):
    """Show details for a specific booking."""
    booking = get_object_or_404(Booking, id=id, customer=request.user)
    total_cost = booking.ticket_count * booking.unit_price
    return render(request, BASE_TEMPLATE_PATH + 'detail.html', {
        "booking": booking,
        "total_cost": total_cost,
        "status_label": booking.get_status_display()
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