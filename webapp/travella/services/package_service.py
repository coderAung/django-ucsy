from datetime import date, timedelta
import uuid
from django.http import QueryDict
from django.db import transaction
from django.db.models import Q, QuerySet
from django.core.files.uploadedfile import UploadedFile
from django.core.paginator import Paginator, Page
from django.db.models import Sum
from travella.domains.models.account_models import Account
from travella.dtos.package_card import PackageCard, PackageDetail
from travella.dtos.package_form import PackageForm
from travella.dtos.package_search import PackageSearch, PublicPackageSearch
from travella.services.package_utils import is_empty
from travella.dtos.api_dtos import BookingOverview
from travella.utils.pagination import SIZE, PaginationResult
from ..domains.models.booking_models import Booking
from ..domains.models.tour_models import Category, Package, PackageData, Photo
from ..dtos.package_dto import PackageItem, PackageItemDetail


class PackageService:

    def generate_code(self, cid:int) -> str:
        last_code_str:str = (Package.objects
                         .filter(category_id = cid)
                         .order_by('-code')
                         .values('code')
                         .first())['code']
        prefix = last_code_str[:4]
        last_code = int(last_code_str.removeprefix(prefix))

        new_code = last_code + 1
        new_code_str = str(new_code).zfill(3)
        cname = Category.objects.get(pk = cid).name
        return f'{prefix}{new_code_str}', cname

    def get_all(self) -> list[PackageItem]:
        packages = Package.objects.all()
        items = [PackageItem.of(p) for p in packages]
        return items

    def get_one(self, code:str) -> PackageItemDetail:
        package = Package.objects.get(code = code)
        return PackageItemDetail.of(package)
    
    def get_gallery(self, code:str) -> list[str]:
        photos:QuerySet[Photo] = Package.objects.get(code = code).photos.all()
        return [p.path.url for p in photos]

    def search_list(self, search:PackageSearch) -> PaginationResult:
        packages = Package.objects.filter(search.filter()).order_by('-created_at')
        paginator = Paginator(packages, 6)
        return PaginationResult(search.page, paginator, PackageItem.of)

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
        qs = Package.objects.filter(qf).order_by('-created_at')
        if not is_empty(status):
            qs = [q for q in qs if q.data.status == status]        
        return [PackageItem.of(p) for p in qs]
    
    def booking_overview(self, id:uuid) -> BookingOverview:
        booking = Booking.objects.filter(id = id).first()
        return BookingOverview.of(booking)
    
    def save(self, account:Account, form:PackageForm, images:list[UploadedFile]) -> str:
        package:Package = form.to_model(account)
        package.save()
        PackageData(code=package.code, remaining_tickets=package.total_tickets, package=package).save()
        for i in images:
            Photo.objects.create(package=package, path=i)
        return package.code
    
    def delete(self, code:str):
        package = Package.objects.get(code = code)
        with transaction.atomic():
            for p in package.photos.all():
                p.path.delete(save = False)
            package.delete()

    def search_for_customer(self, search:PublicPackageSearch)  -> PaginationResult:
        packages = Package.objects.filter(Q(data__status=PackageData.Status.AVAILABLE) & search.filter()).order_by('-created_at')
        pagination = Paginator(packages, SIZE)
        paginationResult = PaginationResult(search.page, pagination, PackageCard.of)
        return paginationResult

    def count(self) -> int:
        return Package.objects.count()
    
    def detail(self, code:str) -> PackageDetail:
        package = Package.objects.get(code = code)
        dto = PackageDetail.of(package)
        return dto
    
from django.db.models import Sum
from travella.domains.models.booking_models import Booking

def duration_by_code(code:str) -> int:
    result = Package.objects.filter(code = code).values('duration').first()
    return result['duration']

def get_packages_with_availability():
    packages = Package.objects.select_related('category').all()
    
    package_list = []
    for package in packages:
        # Calculate available tickets
        booked_tickets = Booking.objects.filter(
            package=package
        ).exclude(
            status=Booking.Status.CANCELLED
        ).aggregate(
            total=Sum('ticketCount')
        )['total'] or 0
        
        available_tickets = max(0, package.availableTicket - booked_tickets)
        
        package_list.append({
            'code': package.code,
            'name': package.title,
            'category': package.category.name,
            'duration': package.duration,
            'departure': package.departure,
            'tickets': available_tickets,  # Show available tickets instead of total
            'total_capacity': package.availableTicket,  # Keep total for reference if needed
            'status': package.status,
            'price': package.price,
            'bookings': package.booking_count  # This should already be defined in your model
        })
    
    return package_list

