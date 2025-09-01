from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from travella.services.dashboard_service import get_dashboard_data
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request:HttpRequest) -> HttpResponse:
    
    data = get_dashboard_data()
    return render(request, 'admin/dashboard.html', {'data': data})