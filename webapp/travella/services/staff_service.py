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

    staff_member = Account.objects.select_related('accountdetail').prefetch_related('access_logs').get(
        pk=account_id,
        role__in=['admin', 'mod', 'Admin', 'Mod']  # Include capitalized versions for safety
    )
    return staff_member