from django.urls import path

from travella.controllers.auth import auth_controller


urlpatterns = [
    path('sign-in/', auth_controller.sign_in),
    path('sign-out/', auth_controller.sign_out, name='sign_out'),
]