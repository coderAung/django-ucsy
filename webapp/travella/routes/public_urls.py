from django.urls import path
from travella.controllers.public import public_controller
from travella.controllers.customer import review_controller
from travella.controllers.public import discover_controller


urlpatterns = [
    path('discover/', discover_controller.discover, name='discover'),
    path('packages/', public_controller.packages, name='customer_packages'),
    path('packages/<str:code>', public_controller.package_detail, name='public_packages_code'),

    path('reviews/', review_controller.list, name='review_list'),
    path('reviews/<int:id>/', review_controller.detail),

]