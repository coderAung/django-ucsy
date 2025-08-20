from datetime import date, timedelta
import uuid
from django.http import QueryDict
from django.db.models import Q

from travella.services.package_utils import is_empty
from travella.dtos.api_dtos import BookingOverview
from ..domains.models.booking_models import Booking
from ..domains.models.tour_models import Package
from ..dtos.package_dto import PackageItem, PackageDetail


class PackageService:

    def get_all(self) -> list[PackageItem]:
        packages = Package.objects.all()
        items = [PackageItem.of(p) for p in packages]
        return items

    def get_one(self, code:str) -> PackageDetail:
        package = Package.objects.get(code = code)
        return PackageDetail.of(package)

    def search(self, query:QueryDict) -> list[PackageItem]:
        category = query.get('category')
        month = query.get('month')
        status = query.get('status')
        q = query.get('q')
        qf = Q() #qf = queryFilter
        if not is_empty(category):
            qf &= Q(category__name = category)
        if not is_empty(month):
            today = date.today()
            this_month_start = today.replace(day=1)
            this_month_end = today
            last_month_end = today.replace(day=1) - timedelta(days=1)
            last_month_start = last_month_end.replace(day=1)
            if month == 'thisMonth':
                qf &= Q(createdAt__gte = this_month_start, createdAt__lte = this_month_end)
            elif month == 'lastMonth':
                qf &= Q(createdAt__gte = last_month_start, createdAt__lte = last_month_end)
        if not is_empty(q):
            qf &= Q(code__startswith=q.lower()) | Q(title__startswith=q.lower())
        qs = Package.objects.filter(qf)
        if not is_empty(status):
            qs = [q for q in qs if q.status == status]        
        return [PackageItem.of(p) for p in qs]
    
    def booking_overview(self, id:uuid) -> BookingOverview:
        booking = Booking.objects.filter(id = id).first()
        return BookingOverview.of(booking)