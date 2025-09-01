from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from travella.services import itinerary_service


@require_POST
def delete(request:HttpRequest, code:str) -> HttpResponse:
    itinerary_service.delete_by_id(request.POST.get('dayId'))
    return redirect('edit_itinerary', code=code)