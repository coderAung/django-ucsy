from django.urls import path

from ..controllers.admin import dashboard_controller


urlpatterns = [
    path('dashboard/', dashboard_controller.dashboard),
]