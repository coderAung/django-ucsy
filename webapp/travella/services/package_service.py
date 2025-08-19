from datetime import date, timedelta
import uuid
from django.http import QueryDict
from django.db import transaction
from django.db.models import Q, QuerySet
from django.core.files.uploadedfile import UploadedFile
from django.core.paginator import Paginator, Page

from travella.domains.models.account_models import Account
from travella.dtos.package_card import PackageCard
from travella.dtos.package_form import PackageForm
from travella.services.package_utils import is_empty
from travella.dtos.api_dtos import BookingOverview
from travella.utils.pagination import PaginationResult
from ..domains.models.booking_models import Booking
from ..domains.models.tour_models import Category, Package, Photo
from ..dtos.package_dto import PackageItem, PackageDetail


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

    def get_one(self, code:str) -> PackageDetail:
        package = Package.objects.get(code = code)
        return PackageDetail.of(package)
    
    def get_gallery(self, code:str) -> list[str]:
        photos:QuerySet[Photo] = Package.objects.get(code = code).photos.all()
        return [p.path.url for p in photos]

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
        qs = Package.objects.filter(qf).order_by('-createdAt')
        if not is_empty(status):
            qs = [q for q in qs if q.status == status]        
        return [PackageItem.of(p) for p in qs]
    
    def booking_overview(self, id:uuid) -> BookingOverview:
        booking = Booking.objects.filter(id = id).first()
        return BookingOverview.of(booking)
    
    def save(self, account:Account, form:PackageForm, images:list[UploadedFile]) -> bool:
        print(form.departure)
        package:Package = form.to_model(account)
        package.save()
        for i in images:
            Photo.objects.create(package=package, path=i)
        return True
    
    def delete(self, code:str):
        package = Package.objects.get(code = code)
        with transaction.atomic():
            for p in package.photos.all():
                p.path.delete(save = False)
            package.delete()

    def search_for_customer(self)  -> PaginationResult:
        packages = Package.objects.all().order_by('-createdAt')
        pagination = Paginator(packages, 2)
        paginationResult = PaginationResult(2, pagination, PackageCard.of)
        # cards = [PackageCard.of(p) for p in packages]
        return paginationResult
