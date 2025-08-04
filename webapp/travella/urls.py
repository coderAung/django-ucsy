from django.urls import path, include

from .routes import customer_urls, admin_urls,auth_urls, test_urls

urlpatterns = [
    path('', include(auth_urls)),
    path('admins/', include(admin_urls)),
    path('customer/', include(customer_urls)),
    path('public/', include(public_urls)),
    path('auth/', include(auth_urls)),
    path('test/', include(test_urls)),
]