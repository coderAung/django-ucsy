from django.urls import path

from ..controllers import test_controller

urlpatterns = [
    path('home/', test_controller.home),
    path('setting/', test_controller.setting)
]