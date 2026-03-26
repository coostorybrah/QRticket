from django.urls import path
from .views import api_pay_order, api_cancel_order, api_create_order, api_my_tickets

urlpatterns = [
    path("<int:order_id>/pay/", api_pay_order),
    path("<int:order_id>/cancel/", api_cancel_order),
    path("create/", api_create_order),
    path("my-tickets/", api_my_tickets),
]