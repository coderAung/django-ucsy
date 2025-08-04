from django.urls import path, include

from .routes import customer_urls, admin_urls,auth_urls, test_urls

urlpatterns = [
    path('', include(auth_urls)),
    path('admins/', include(admin_urls)),
    path('customers/', include(customer_urls)),
    path('test/', include(test_urls)),
]