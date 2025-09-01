from django.urls import path

from travella.controllers.auth import auth_controller
from travella.controllers.auth.signup_controller import SignUpView

urlpatterns = [
    path('sign-in/', auth_controller.sign_in, name='sign_in'),
    path('sign-out/', auth_controller.sign_out, name='sign_out'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
]