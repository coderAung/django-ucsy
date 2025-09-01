from django.shortcuts import render
from travella.models import Booking, Package, Account,Review
from ..dtos.dashboardDTO import DashboardDTO
from travella.dtos.dashboardDTO import DashboardDTO
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.db.models import F, Sum, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth
from django.db.models import F, Sum, ExpressionWrapper, DecimalField
from decimal import Decimal

def get_dashboard_data():
  total_bookings = Booking.objects.count()
  total_packages = Package.objects.count()
  
  one_mth_ago = timezone.now() - timedelta(days=30)
  one_yr_ago = timezone.now() - timedelta(days = 365)
  new_customers = Account.objects.filter(created_at__gte = one_mth_ago).count()
  active_customers = Account.objects.filter(created_at__gte = one_yr_ago).count()

  top_packages = Package.objects.annotate(total_bookings_1pkg=Count('bookings')).order_by('-total_bookings_1pkg')[:5]

  top_packages_data = [
    {'name':pkg.title, 'count': pkg.total_bookings_1pkg}
    for pkg in top_packages
  ]

  pending_bookings = Booking.objects.filter(status = Booking.Status.PENDING).count()
  cancel_bookings = Booking.objects.filter(status = Booking.Status.CANCELLED).count()
  pending_payment = Booking.objects.filter(
    status=Booking.Status.RESERVED
    ).aggregate(
    total=Sum(
        ExpressionWrapper(
            F('ticket_count') * F('unit_price'),
            output_field=DecimalField(max_digits=12, decimal_places=2)
        )
    )
  )['total'] or Decimal('0')

  pending_payment = "{:,.2f}".format(Decimal(pending_payment).quantize(Decimal('0.01')))
  
  total_feedbacks = Review.objects.count()

# --- NEW: Monthly bookings for chart ---
  monthly_bookings_data = (
        Booking.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(bookings=Count('id'))
        .order_by('month')
  )
  chart_data = [
          {"month": item['month'].strftime("%b %Y"), "bookings": item['bookings']}
          for item in monthly_bookings_data
  ]
  return render(request, 'admin/dashboard.html', {
        'data': data,
        'chart_data': chart_data
    })

  return DashboardDTO(
    total_bookings = total_bookings,
    total_packages= total_packages,
    new_customers = new_customers,
    active_customers = active_customers,
    top_packages = top_packages_data,
    pending_bookings = pending_bookings,
    cancel_bookings = cancel_bookings,
    pending_payment = pending_payment,
    total_feedbacks = total_feedbacks,
    monthly_bookings= monthly_bookings_data
    )