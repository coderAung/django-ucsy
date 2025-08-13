from datetime import date, datetime
import decimal

from django.http import QueryDict

from travella.domains.models.tour_models import Package


class PackageForm:
    code:str
    cid:int
    name:str
    departure:date
    duration:int
    ticket:int
    price:decimal
    overview:str

    @staticmethod
    def of(post:QueryDict) -> 'PackageForm':
        form = PackageForm()
        form.code = post.get('code')
        form.cid = int(post.get('cid'))
        form.name = post.get('name')
        form.departure = datetime.strptime(post.get('departure'), "%Y-%m-%d").date()
        form.overview = post.get('overview')
        form.duration = post.get('departure')
        form.price = decimal.Decimal(post.get('price'))
        form.ticket = post.get('ticket')
        return form
        
    def __str__(self):
        return (f'PackageForm(code={self.code}, cid={self.cid}, name={self.name}, '
                f'duration={self.duration}, departure={self.departure}'
                f'ticket={self.ticket}, price={self.price}, overview={self.overview})')