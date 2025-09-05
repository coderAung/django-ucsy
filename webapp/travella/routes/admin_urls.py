from tkinter.font import names

from django.urls import path

from travella.controllers.admin import chat_controller
from travella.controllers.admin.managements import itinerary_controller, refund_request_controller, reservation_controller

from ..controllers.admin.managements import booking_controller, category_controller, package_controller, \
    customer_controller, staff_controller, package_form_api

from ..controllers.admin import dashboard_controller, location_controller

from ..controllers.admin.settings import setting_controller, account_controller


urlpatterns = [
    path('dashboard/', dashboard_controller.dashboard, name = 'dashboard'),
    path('bookings/', booking_controller.list, name = 'bookings'),
    path('bookings/<uuid:id>/', booking_controller.detail, name='booking_detail'),

    path('categories/', category_controller.list, name='categories'),
    path('categories/new/', category_controller.new, name='category-new'),
    path('categories/save/', category_controller.save, name='create_category'),
    path('categories/<int:id>/edit/', category_controller.edit, name='edit_category'),
    path('categories/<int:id>/delete/', category_controller.delete, name='delete_category'),

    path('packages/', package_controller.list, name = 'packages'),
    path('packages/new/', package_controller.new, name='packages_new'),
    path('packages/save/', package_controller.save, name='packages_save'),
    path('packages/new-code/', package_form_api.new_package_code),
    path('packages/delete/', package_controller.delete, name='packages_delete'),
    path('packages/<str:code>/', package_controller.detail, name='packages_detail'),
    path('packages/edit/<str:code>/', package_controller.edit),
    path('packages/edit-itinerary/<str:code>/', package_controller.edit_itinerary, name='edit_itinerary'),
    path('packages/delete-itinerary/<str:code>/', itinerary_controller.delete, name='delete_itinerary'),

    path('locations/', location_controller.location_list, name='location_list'),
    path('locations/add/', location_controller.location_add, name='location_add'),
    path('locations/edit/<int:pk>/', location_controller.location_edit, name='location_edit'),
    path('locations/delete/<int:pk>/', location_controller.location_delete, name='location_delete'),


    path('settings/', setting_controller.settings_home, name = 'settings'),
    path('settings/access-logs/', setting_controller.logs),
    path('settings/account/', setting_controller.account),
    path('settings/account/email/', setting_controller.email),
    path('settings/account/password/', setting_controller.password),

    # POST method only
    path('settings/account/email/change/', account_controller.email, name='settings_account_email_change'),
    path('settings/account/password/change/', account_controller.password, name='settings_account_password_change'),
    path('settings/account/info/', account_controller.info, name='settings_account_info'),

    path('customers/', customer_controller.list, name='customers'),
    path('customers/<uuid:id>/', customer_controller.detail, name='customers_detail'),

    path('staffs/', staff_controller.list, name='staffs'),
    path('staffs/<uuid:id>/', staff_controller.detail, name='staffs_detail'),
    path('staffs/add/', staff_controller.add_staff, name='add_staff'),

    path('reservations/', reservation_controller.get_list, name='reservations'),
    path('reservations/reserve/', reservation_controller.save, name='reservations_reserve'),
    path('reservations/reject/', reservation_controller.reject, name='reservations_reject'),
    path('reservations/<uuid:id>/', reservation_controller.detail, name='reservations_detail'),


    path('refund_requests/', refund_request_controller.get_list, name='refund_requests'),

    path('refund_requests/confirm/', refund_request_controller.confirm, name='refund_confirm'),

    path('refund_requests/<uuid:id>', refund_request_controller.detail, name='refund_requests_detail'),

    path('chats/', chat_controller.chat_list, name='chat_list'),
    path('chats/<uuid:id>/', chat_controller.chat_room, name='chat_room'),
]