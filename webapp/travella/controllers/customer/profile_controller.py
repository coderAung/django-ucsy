from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from travella.exceptions.business_exception import BusinessException
from travella.services import customer_profile_service, profile_image_service
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