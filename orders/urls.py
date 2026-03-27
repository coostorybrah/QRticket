from django.urls import path
import orders.views as views

urlpatterns = [
    path("<int:order_id>/pay/", views.api_pay_order),
    path("<int:order_id>/cancel/", views.api_cancel_order),
    path("create/", views.api_create_order),
    path("my-tickets/", views.api_my_tickets),
    path("<int:order_id>/add-items/", views.api_add_items),
    path("payment-return/", views.payment_return),
]