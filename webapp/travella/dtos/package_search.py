from datetime import date, datetime

from django.http import QueryDict


class PublicPackageSearch:
    categoryId:int = 0
    locationId:int = 0
    departureFrom:date
    departureTo:date
    q:str = ''
    page:int = 1

    def __init__(self, categoryId = 0, locationId = 0, departureFrom:date = None, departureTo:date = None, q = '', page = 1):
        self.categoryId = categoryId
        self.locationId = locationId
        self.departureFrom = departureFrom
        self.departureTo = departureTo
        self.q = q
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
        return form
