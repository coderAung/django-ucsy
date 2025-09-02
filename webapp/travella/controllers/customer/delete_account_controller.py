from urllib.parse import urlencode
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from travella.exceptions.business_exception import BusinessException
from travella.services import account_delete_service


def delete(request:HttpRequest) -> HttpResponse:
    password = request.POST.get('password', '')
    try:
        account_delete_service.delete(request.user.id, password)
        logout(request)
        return redirect('discover')
    except BusinessException as e:
        messages.error(request, e.get_message())
        base_url = reverse('customer_settings')
        query = urlencode({'p': 'd'})
        return redirect(f'{base_url}?{query}')