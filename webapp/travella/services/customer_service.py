from ..domains.models.account_models import Account
from django.db.models import Q, QuerySet


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
