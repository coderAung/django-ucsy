import uuid
from django.http import HttpRequest, QueryDict
from django.db.models import Q
from django.contrib import messages

from travella.domains.models.booking_models import Booking
from travella.exceptions.business_exception import BusinessException
from travella.services.package_utils import is_empty
from travella.utils.validation import is_valid_uuid


class ReservationSearch:
    
    def __init__(self, request:HttpRequest):
        self._request = request
        query:QueryDict = request.GET
        self.type = query.get('type') if not is_empty(query.get('type')) else 'email'
        self.q = query.get('q') if not is_empty(query.get('q')) else ''
        self.payment_status = query.get('payment_status') if not is_empty(query.get('payment_status')) else 'requesting'

    def search(self) -> Q:
        q = Q()
        if not is_empty(self.q):
            if self.type == 'email':
                q &= Q(customer__email__startswith=self.q)
            elif self.type == 'booking_code':
                is_valid, message = is_valid_uuid(self.q, f'Invalid Booking Code : {self.q}')
                if is_valid:
                    q &= Q(booking__id=uuid.UUID(self.q))
                else:
                    messages.error(self._request, message)
        if self.payment_status == 'reserved':
            q &= Q(booking__status = Booking.Status.RESERVED)
        else:
            q &= Q(is_reserved = False)
        return q
    