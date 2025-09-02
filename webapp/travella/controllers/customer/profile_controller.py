from urllib.parse import urlencode
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib import messages

from travella.exceptions.business_exception import BusinessException
from travella.services import account_service, customer_profile_service, profile_image_service
from travella.utils.route_view import RouteView

view = RouteView.get('customer/')

def profile(request:HttpRequest) -> HttpResponse:
    try:
        print(f'====={request.user.id}=====')
        profile_data = customer_profile_service.get_profile_data(request)
        booking_status = customer_profile_service.get_booking_status_by_account_id(profile_data.id)
        tour_reminders = customer_profile_service.get_tour_reminders_by_account_id(profile_data.id)
        return render(request, view('profile'), {
            'profile_data': profile_data,
            'booking_status': booking_status,
            'tour_reminders': tour_reminders,
        })
    except ValueError as e:
        raise BusinessException('Profile not found.')

@require_POST
def upload_profile_image(request:HttpRequest) -> JsonResponse:
    try:
        url = profile_image_service.upload(request)
        return JsonResponse({
            'success': True,
            'url': url,
        })
    except BusinessException as e:
        return JsonResponse({
            'success': False,
            'message': e.get_message() 
        })
    
@require_POST
def update_profile(request:HttpRequest) -> HttpResponse:
    post = request.POST
    name = post.get('name', '')
    phone = post.get('phone', '')
    address = post.get('address', '')
    if not name and not phone and not address:
        return redirect('customer_settings')
    customer_profile_service.update(request.user.id, name, phone, address)
    
    return redirect('customer_settings') 

@require_POST
def change_password(request:HttpRequest) -> HttpResponse:
    post = request.POST
    old_password = post.get('oldPassword', '')
    new_password = post.get('newPassword', '')
    try:
        account_service.update_account_password(request.user, old_password, new_password)    
    except BusinessException as e:
        messages.error(request, e.get_message())
    base_url = reverse('customer_settings')
    query = urlencode({'p': 'password'})
    return redirect(f'{base_url}?{query}')