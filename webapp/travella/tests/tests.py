from django.db.models import Q

from travella.domains.models.booking_models import Booking
from travella.domains.models.tour_models import Package, PackageData

def load_package_data():
    packages = Package.objects.all()
    for p in packages:
        booked_tickets = p.booking_count
        the_count = PackageData.objects.filter(code = p.code).count()
        if the_count == 0:
            PackageData(code = p.code, remaining_tickets = p.total_tickets - booked_tickets, package = p).save()
