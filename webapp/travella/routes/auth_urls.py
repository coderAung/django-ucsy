from django.urls import path

from travella.controllers.auth import auth_controller


urlpatterns = [
    path('sign-in/', auth_controller.sign_in)
]