from django.urls import path, include

from travella.routes import auth_urls

from .routes import customer_urls, admin_urls, test_urls

urlpatterns = [
    path('admins/', include(admin_urls)),
    path('customers/', include(customer_urls)),
    path('auth/', include(auth_urls)),
    path('test/', include(test_urls)),
]