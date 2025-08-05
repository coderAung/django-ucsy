from django.urls import path

from ..controllers.admin.managements import booking_controller, category_controller, package_controller, customer_controller

from ..controllers.admin import dashboard_controller

from ..controllers.admin.settings import setting_controller, account_controller


urlpatterns = [
    path('dashboard/', dashboard_controller.dashboard, name = 'dashboard'),
    path('bookings/', booking_controller.list, name = 'bookings'),
   path('bookings/<uuid:id>/', booking_controller.detail, name='booking_detail'),



    path('categories/', category_controller.list, name = 'categories'),
    path('categories/<int:id>/', category_controller.detail),
    path('categories/new/', category_controller.new),
    path('categories/save', category_controller.save),
    path('categories/<int:id>/edit', category_controller.edit),

    path('packages/', package_controller.list, name = 'packages'),
    path('packages/<int:id>/', package_controller.detail),
    path('packages/new/', package_controller.new),
    path('packages/save/', package_controller.save),
    path('packages/<int:id>/edit', package_controller.edit),

    # GET method only
    path('settings/', setting_controller.list, name = 'settings'),
    path('settings/access-logs/', setting_controller.logs),
    path('settings/account/', setting_controller.account),
    path('settings/account/email/', setting_controller.email),
    path('settings/account/password/', setting_controller.password),

    # POST method only
    path('settings/account/email/change/', account_controller.email),
    path('settings/account/password/change/', account_controller.password),
    path('settings/account/photo/', account_controller.photo),
    path('settings/account/info/', account_controller.info),

    path('users/', customer_controller.list),
    path('users/<int:id>/', customer_controller.detail),
]