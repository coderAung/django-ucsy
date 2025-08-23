from travella.models import Booking, Package, Account,Review
from ..dtos.dashboardDTO import DashboardDTO
from travella.dtos.dashboardDTO import DashboardDTO
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.db.models import F, Sum, ExpressionWrapper, DecimalField

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
  pending_payment = Booking.objects.filter(status=Booking.Status.RESERVED).aggregate(
    total=Sum(
        ExpressionWrapper(
            F('ticket_count') * F('unit_price'),
            output_field=DecimalField()
        )
    )
)['total'] or 0
  
  total_feedbacks = Review.objects.count()

  return DashboardDTO(
    total_bookings = total_bookings,
    total_packages= total_packages,
    new_customers = new_customers,
    active_customers = active_customers,
    top_packages = top_packages,
    pending_bookings = pending_bookings,
    cancel_bookings = cancel_bookings,
    pending_payment = pending_payment,
    total_feedbacks = total_feedbacks
    )