# C:\BookTour\webapp\travella\controllers\admin\settings\setting_controller.py

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from travella.domains.models.log_models import AccessLog
from travella.domains.models.account_models import Account # ADD THIS IMPORT

base = 'admin/settings/'

def view(name:str) -> str:
    return base + name + '.html'

# settings/ main page
def settings_home(request:HttpRequest) -> HttpResponse:
    """
    Handles the base /settings/ URL and redirects to the account page.
    """
    return redirect('/admins/settings/account')

# settings/account/ main page
def account(request: HttpRequest) -> HttpResponse:
    """
    Renders the main account settings page with the current user's data.
    """
    context = {
        'user': request.user
    }
    return render(request, view('account'), context)

# settings/account/info POST
@require_POST
def info(request:HttpRequest) -> HttpResponse:
    """
    Processes the single form from the account.html template.
    This function handles both personal info and profile photo updates.
    """
    user = request.user
    
    # Update personal information from the form data
    user.name = request.POST.get('name')
    user.phone = request.POST.get('phone')
    user.address = request.POST.get('address')
    
    # Handle profile image upload
    if 'profile_image' in request.FILES:
        profile_image = request.FILES['profile_image']
        # Note: You need to implement your own file saving logic here.
        # Example: user.photo_url = save_file(profile_image)
        pass

    # Save the updated user information
    user.save()
    
    # Redirect back to the account settings page
    return redirect('/admins/settings/account')


# settings/account/photo POST
@require_POST
def photo(request:HttpRequest) -> HttpResponse:
    """
    This view is a placeholder. The unified form in account.html
    has consolidated the photo upload logic into the 'info' view.
    """
    return redirect('/admins/settings/account')

# settings/account/email/chage POST
@require_POST
def email(request:HttpRequest) -> HttpResponse:
    """
    Handles email change form submission.
    (Placeholder for logic to change email, send verification, etc.)
    """
    return redirect('/admins/settings/account/email')

# settings/account/password/change POST
@require_POST
def password(request:HttpRequest) -> HttpResponse:
    """
    Handles password change form submission.
    (Placeholder for logic to change password)
    """
    return redirect('/admins/settings/account/password')

# settings/access-logs GET
def logs(request: HttpRequest) -> HttpResponse:
    """
    Renders the access logs page for the currently logged-in admin user.
    """
    # Assuming request.user is an authenticated user object
    access_logs = AccessLog.objects.filter(account=request.user).order_by('-created_at')
    
    context = {
        'access_logs': access_logs
    }
    
    return render(request, view('access-logs'), context)
    


def staff_detail(request, staff_id: str):
    """
    Renders the staff detail page with their information and access logs.
    """
    staff = get_object_or_404(Account, id=staff_id)
    
    # This is the line that fixes the ordering
    staff_access_logs = AccessLog.objects.filter(account=staff).order_by('-created_at')[:5]
    
    context = {
        'staff': staff,
        'staff_access_logs': staff_access_logs,
    }
    return render(request, 'admin/managements/users/staff-detail.html', context)