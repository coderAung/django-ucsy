from datetime import date, datetime

from django.http import HttpRequest, QueryDict
from django.db.models import Q

from travella.domains.models.tour_models import PackageData
from travella.services.package_utils import is_empty


class PublicPackageSearch:
    categoryId:int = 0
    locationId:int = 0
    minPrice: int = 0
    maxPrice: int = 0
    departureFrom:date = None
    departureTo:date = None
    q:str = ''
    page:int = 1

    def __init__(self, page = 1):
        self.page = page

    def __str__(self):
        return f'{self.categoryId}, {self.locationId}, {self.departureFrom}, {self.departureTo}, {self.q}, {self.page}'

    @staticmethod
    def of(query:QueryDict) -> 'PublicPackageSearch':
        form = PublicPackageSearch()
        if query.get('categoryId') != '' and query.get('categoryId') != None:
            form.categoryId = int(query.get('categoryId'))
        if query.get('locationId') != '' and query.get('locationId') != None:
            form.locationId = int(query.get('locationId'))
        if (query.get('fromDate') != '' and query.get('fromDate') != None) and (query.get('toDate') and query.get('toDate') != None):
            form.departureFrom = datetime.strptime(query.get('fromDate'), "%Y-%m-%d").date()
            form.departureTo = datetime.strptime(query.get('toDate'), "%Y-%m-%d").date()
        if query.get('q') != '' and query.get('q') != None:
            form.page = query.get('q')
        if query.get('page') != '' and query.get('page') != None:
            form.page = int(query.get('page'))
        if query.get('price') != '' and query.get('price') is not None:
            price_range = query.get('price')
            if '-' in price_range:
                min_str, max_str = price_range.split('-')
            
                if min_str:
                    form.minPrice = int(min_str)
                if max_str:
                    form.maxPrice = int(max_str)
        return form
    
    def filter(self) -> Q:
        qf = Q()
        if None != self.categoryId and self.categoryId != 0:
            qf &= Q(category__id = self.categoryId)
        if None != self.locationId and self.locationId != 0:
            qf &= Q(location__id = self.locationId)
        if not is_empty(self.q):
            qf &= Q(title__startswith = self.q.lower())
        if self.departureFrom and self.departureTo:
            qf &= Q(departure__gte = self.departureFrom, departure__lte = self.departureTo)
        if self.minPrice > 0 and self.maxPrice > 0:
            qf &= Q(price__gte=self.minPrice, price__lte=self.maxPrice)
        elif self.minPrice > 0:
            qf &= Q(price__gte=self.minPrice)
        elif self.maxPrice > 0:
            qf &= Q(price__lte=self.maxPrice)

        return qf


class PackageSearch:
    category:str
    locationId:int = 0
    status:str = ''
    departure_from:date = None
    departure_to:date = None
    q:str = ''
    page:int = 1

    def __init__(self, request:HttpRequest):
        query = request.GET
        self.category = query.get('category')
        self.status = query.get('status')
        self.q = query.get('q')
        if not is_empty(query.get('from')):
            self.departure_from = datetime.strptime(query.get('from'), "%Y-%m-%d").date() 
        if query.get('to'):
            self.departure_to = datetime.strptime(query.get('to'), "%Y-%m-%d").date() 
        if query.get('page'):
            self.page = int(query.get('page'))

    def filter(self) -> Q:
        q = Q()
        if not is_empty(self.category):
            q &= Q(category__name = self.category)
        if not is_empty(self.status):
            try:
                q &= Q(data__status = PackageData.Status(self.status))
            except ValueError as e:
                pass
        if not is_empty(self.q):
            q &= Q(code__startswith = self.q.lower()) | Q(title__startswith = self.q.lower())
        if self.departure_from:
            q &= Q(departure__gte = self.departure_from)
        if self.departure_to:
            q &= Q(departure__lte = self.departure_to)

        return q