from django.urls import path
from . import views

urlpatterns = [
    path("paypal-webhook/", views.paypal_webhook),
    path("find-order/", views.find_order_by_paypal),
]