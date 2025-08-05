from django.urls import path

from travella.controllers.admin.managements import package_controller

from ..controllers import test_controller

urlpatterns = [
    path('home/', test_controller.home),
    path('setting/', test_controller.setting),
    path('overview/<uuid:id>', package_controller.booking_overview)
]