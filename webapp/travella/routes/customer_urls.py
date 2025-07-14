from django.urls import path

from ..controllers.customer import home_controller

urlpatterns = [
    path('home/', home_controller.home),
]