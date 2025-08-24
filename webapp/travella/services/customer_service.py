from django.shortcuts import get_object_or_404

from ..domains.models.account_models import Account
from django.db.models import Q, QuerySet

from ..domains.models.booking_models import Booking


def get_all_customers() -> QuerySet[Account]:

    return Account.objects.select_related('accountdetail').filter(role=Account.Role.CUSTOMER)


def get_filtered_customers(query: str) -> QuerySet[Account]:

    base_queryset = get_all_customers()

    if not query:
        return base_queryset

    return base_queryset.filter(
        Q(accountdetail__name__icontains=query) |
        Q(email__icontains=query) |
        Q(accountdetail__phone__icontains=query)
    ).distinct()

def get_customer_detail(account_id: str) -> Account:
    customer = get_object_or_404(
        Account.objects.select_related('accountdetail'),
        pk=account_id,
        role=Account.Role.CUSTOMER
    )
    return customer

def get_bookings_for_customer(customer_account: Account) -> QuerySet[Booking]:
    # Change 'account' to 'customer' to match the actual field name in your Booking model
    return Booking.objects.filter(customer=customer_account).order_by('-createdAt')
