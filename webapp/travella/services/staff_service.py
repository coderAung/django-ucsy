from django.shortcuts import get_object_or_404
from django.db import transaction
from ..domains.models.account_models import AccountDetail
from ..domains.models.account_models import Account
from django.db.models import Q, QuerySet
def get_all_staff() -> QuerySet[Account]:
    return Account.objects.select_related('accountdetail').filter(
        Q(role__iexact='admin') | Q(role__iexact='mod')
    )

def get_filtered_staff(query: str = None, role: str = None) -> QuerySet[Account]:

    q = Q()
    if query != '' and query != None:
        q &= (Q(accountdetail__name__startswith=query) | Q(email__startswith=query))

    if role != '' and role != None:
        q &= Q(role = Account.Role(role))
    else:
        q &= (Q(role=Account.Role.ADMIN ) | Q(role = Account.Role.MOD))

    base_queryset = Account.objects.filter(q)
    for b in base_queryset:
        print(b.email, b.role)
    return base_queryset


def get_staff_detail(account_id: str) -> Account:

    staff_member = get_object_or_404(
        Account.objects.select_related('accountdetail').prefetch_related('access_logs'),
        pk=account_id,
        role__in=['admin', 'mod', 'Admin', 'Mod']
    )
    return staff_member

def create_staff(name, email, password, role, creator):
    try:
        with transaction.atomic():
            new_staff_account = Account.objects.create_user(email=email, password=password, role=role, created_by=creator )
            AccountDetail.objects.create(account=new_staff_account, name=name)
            return new_staff_account
    except Exception as e:
        print(f"Error creating staff: {e}")
        return None