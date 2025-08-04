from django.urls import path
from ..controllers.admin.managements import auth_controller

urlpatterns = [
    path('login/', auth_controller.admin_login, name='login'),
    path('logout/', auth_controller.logout, name='logout'),
    path('setup-admin/', auth_controller.setup_admin, name='setup_admin'),
]
