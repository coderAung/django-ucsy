from django.urls import path
from django.shortcuts import render
from ..controllers.customer import review_controller, booking_controller, reservation_controller

urlpatterns = [
    path('packages/book/<str:code>/', booking_controller.new, name='packages_book'),
    path("test-form/", lambda request: render(request, "customer/bookings/form.html")),
    path('bookings/save/', booking_controller.save, name='booking_save'),
    
    path('bookings/history/', booking_controller.history, name='customer_booking_history'),
    path('bookings/<uuid:id>', booking_controller.detail),

    path('bookings/reserve/<uuid:id>', reservation_controller.new),

    path('reservations/', reservation_controller.history),
    path('reservations/<int:id>/', reservation_controller.voucher),

    path('reviews/', review_controller.list, name='review_list'),
    path('reviews/new/', review_controller.new, name='create_review'),
    path('reviews/save/', review_controller.save, name='save_review'),
    path('customer/reviews/edit/<uuid:id>/', review_controller.edit, name='edit_review'),
    path('customer/reviews/delete/<uuid:id>/', review_controller.delete, name='delete_review'),
]