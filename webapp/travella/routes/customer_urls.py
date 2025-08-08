from django.urls import path

from ..controllers.customer import review_controller, booking_controller, reservation_controller

urlpatterns = [
    path('packages/book/<str:code>/', booking_controller.new),
    path('bookings/save', booking_controller.save),

    path('bookings/', booking_controller.history),
    path('bookings/<uuid:id>', booking_controller.detail),

    path('bookings/reserve/<uuid:id>', reservation_controller.save),

    path('reservations/', reservation_controller.history),
    path('reservations/<int:id>/', reservation_controller.voucher),

    path('reviews/new/', review_controller.new),
    path('reviews/edit/<int:id>/', review_controller.edit),
    path('reviews/save/', review_controller.save),
    path('reviews/delete/<int:id>', review_controller.delete),
]