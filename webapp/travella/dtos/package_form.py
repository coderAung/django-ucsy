from datetime import date, datetime
import decimal

from django.http import QueryDict

from travella.domains.models.account_models import Account
from travella.domains.models.tour_models import Category, Location, Package
from travella.utils.validation import FormValidator


class PackageForm:
    code:str
    cid:int
    title:str
    departure:date
    duration:int
    ticket:int
    price:decimal
    location:str
    transportation:Package.Transportation
    overview:str        
    
    def to_model(self, account:Account) -> Package:
        package = Package(
            code=self.code,
            title=self.title,
            departure=self.departure,
            duration=self.duration,
            transportation=self.transportation,
            total_tickets=self.ticket,
            price=self.price,
            overview=self.overview,
            category=Category.objects.get(id=self.cid),
            location=Location.objects.filter(name=self.location).get(),
            created_by=account
            )
        return package

    @staticmethod
    def validate(post:QueryDict) -> dict[str, str]:
        validator = (FormValidator.Builder()
            .rule('code').rule('cid').rule('title')
            .rule('departure').rule('duration').rule('ticket').rule('price')
            .rule('location').rule('transportation')).build()
        return validator.validate(post)

    @staticmethod
    def of(post:QueryDict) -> tuple['PackageForm', dict[str, str]]:
        errors = PackageForm.validate(post)

        form = PackageForm()
        form.code = post.get('code')
        if post.get('cid') != '':
            form.cid = int(post.get('cid'))
        form.title = post.get('title')
        if post.get('departure') != '':
            form.departure = datetime.strptime(post.get('departure'), "%Y-%m-%d").date()
        form.overview = post.get('overview')
        if post.get('duration') != '':
            form.duration = post.get('duration')
        if post.get('price') != '':
            form.price = decimal.Decimal(post.get('price'))
        if post.get('ticket') != '':
            form.ticket = post.get('ticket')
        if post.get('location') != '':
            form.location = post.get('location')
        if post.get('transportation') != '':
            form.transportation = Package.Transportation(int(post.get('transportation')))
        return form, errors