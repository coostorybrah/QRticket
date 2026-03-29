from django.urls import path
import orders.views as views

urlpatterns = [
    path("", views.api_create_order),
    path("<int:order_id>/items/", views.api_add_items),
    path("<int:order_id>/status/", views.api_order_status),
    path("<int:order_id>/pay/", views.api_pay_order),
    path("<int:order_id>/cancel/", views.api_cancel_order),
    path("my-tickets/", views.api_my_tickets),
]