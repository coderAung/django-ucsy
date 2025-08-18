from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from travella.domains.models.tour_models import Package
from travella.domains.models.booking_models import Booking
from travella.domains.models.account_models import AccountDetail

BASE_TEMPLATE_PATH = 'customer/bookings/'

@login_required
def new(request, code: str):
    """Display the booking form for a package."""
    package = get_object_or_404(Package, code=code)

    if package.status != Package.Status.AVAILABLE:
        messages.error(request, "This tour is no longer available for booking.")
        return redirect('customer_booking_history')

    context = {
        'package': package,
        'price_per_seat': f"{package.price:.2f} MMK",
        'price_per_seat_value': float(package.price),
        'departure_date': package.departure.strftime("%B %d, %Y") if package.departure else "N/A",
    }
    return render(request, BASE_TEMPLATE_PATH + 'form.html', context)

@login_required
def history(request):
    """Show all bookings for the current user."""
    bookings = Booking.objects.filter(customer=request.user).select_related('package').order_by('-statusUpdatedAt')
    return render(request, BASE_TEMPLATE_PATH + 'history.html', {
        "bookings": bookings,
        "status_labels": dict(Booking.Status.choices)
    })

@login_required
def detail(request, id):
    """Show details for a specific booking."""
    booking = get_object_or_404(Booking, id=id, customer=request.user)
    total_cost = booking.ticketCount * booking.unitPrice
    return render(request, BASE_TEMPLATE_PATH + 'detail.html', {
        "booking": booking,
        "total_cost": total_cost,
        "status_label": booking.get_status_display()
    })

@login_required
@require_POST
def save(request):
    package_id = request.POST.get('package_id')
    ticket_count = int(request.POST.get('ticketCount', 1))
    package = get_object_or_404(Package, id=package_id)

    # Check package availability
    if package.status != Package.Status.AVAILABLE:
        return JsonResponse({"success": False, "error": "Tour not available"}, status=400)

    # Check remaining seats
    current_booked = Booking.objects.filter(package=package).aggregate(
        total=Sum("ticketCount")
    )["total"] or 0

    if current_booked + ticket_count > package.availableTicket:
        return JsonResponse({"success": False, "error": "Not enough tickets available"}, status=400)

    # ✅ Only one Booking instance, ticketCount = number of people
    booking = Booking.objects.create(
        package=package,
        customer=request.user,
        ticketCount=ticket_count,
        unitPrice=package.price
    )

    return JsonResponse({"success": True, "booking_id": str(booking.id)})
