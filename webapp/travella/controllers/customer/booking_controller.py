from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from travella.domains.models.tour_models import Package
from travella.domains.models.booking_models import Booking

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
        'price_per_seat': f"{int(package.price):,} MMK",
        'departure_date': package.departure.strftime("%B %d, %Y") if package.departure else "N/A",
    }
    return render(request, BASE_TEMPLATE_PATH + 'form.html', context)


@login_required
def history(request):
    """Show all bookings for the current user."""
    bookings = Booking.objects.filter(customer=request.user).order_by('-statusUpdatedAt')
    return render(request, BASE_TEMPLATE_PATH + 'history.html', {"bookings": bookings})


@login_required
def detail(request, id):
    """Show details for a specific booking."""
    booking = get_object_or_404(Booking, id=id, customer=request.user)
    return render(request, BASE_TEMPLATE_PATH + 'detail.html', {"booking": booking})


@require_POST
@login_required
def save(request):
    """Save a new booking from the submitted form."""
    package_id = request.POST.get('package_id')
    ticket_count = int(request.POST.get('ticketCount', 1))

    package = get_object_or_404(Package, id=package_id)

    if package.status != Package.Status.AVAILABLE:
        messages.error(request, "Sorry, this tour is no longer available.")
        return redirect('customer_booking_history')

    if package.booking_count + ticket_count > package.availableTicket:
        messages.error(request, "Not enough tickets available.")
        return redirect('customer_booking_history')

    booking = Booking.objects.create(
        package=package,
        customer=request.user,
        ticketCount=ticket_count,
        unitPrice=package.price
        # status will default to PENDING
    )

    messages.success(request, "Your booking has been submitted and is now pending.")
    return redirect('customer_booking_detail', id=booking.id)
