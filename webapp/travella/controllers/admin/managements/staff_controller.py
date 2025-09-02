import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from ....domains.models.account_models import AccountDetail
from ....services import staff_service
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from travella.domains.models.account_models import Account
from travella.dtos.staff_forms import StaffAddForm
base = 'admin/managements/users/'

def view(name:str) -> str:
    return base + name + '.html'
@login_required
def list(request):
    all_staff_for_check = staff_service.get_all_staff()
    for staff in all_staff_for_check:
        if not hasattr(staff, 'accountdetail'):
            AccountDetail.objects.create(account=staff, name=f"Staff ({staff.role.capitalize()})")
    search_query = request.GET.get('search_query', '').strip()
    role_filter = request.GET.get('role_filter', '').strip()

    staff_qs = staff_service.get_filtered_staff(
        query=search_query,
        role=role_filter
    )
    context = {
        'staff_members': staff_qs,
        'search_query': search_query,
        'role_filter': role_filter,
        'form': StaffAddForm()
    }
    return render(request, view('staff-list'),context)


def detail(request: HttpRequest, id: uuid.UUID) -> HttpResponse:
    try:
        staff_member = staff_service.get_staff_detail(account_id=id)

        # FIX: The logs are now sorted in descending order by created_at.
        staff_access_logs = staff_member.access_logs.all().order_by('-created_at')[:20]

    except staff_service.Account.DoesNotExist:
        return render(request, 'admin/error.html', {'message': 'Staff member not found.'})

    context = {
        'staff': staff_member,
        'staff_access_logs': staff_access_logs
    }
    return render(request, view('staff-detail'),context)


@login_required
def add_staff(request: HttpRequest) -> HttpResponse:
    if request.user.role != Account.Role.ADMIN:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('staffs')

    if request.method == 'POST':
        form = StaffAddForm(request.POST)
        if form.is_valid():
            staff_service.create_staff(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                role=form.cleaned_data['role'],
                creator=request.user
            )
            messages.success(request, 'New staff member added successfully.')
            return redirect('staffs')
        else:
            messages.error(request, 'Please correct the errors below.')
            staff_qs = staff_service.get_filtered_staff(
                query=request.GET.get('search_query', ''),
                role=request.GET.get('role_filter', '')
            )
            context = {'staff_members': staff_qs, 'form': form, 'show_add_staff_modal': True}
            return render(request, view('staff-list'), context)

    return redirect('staffs')