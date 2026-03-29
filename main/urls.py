from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # MAIN PATHS
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("chitietsukien/<str:event_id>/", views.event_detail, name="event_detail"),
    path("orders/<str:event_id>/", views.orders_page, name="orders_page"),
    path("orders-failed/", views.orders_failed, name="orders_failed"),
    path("payment-return/", views.payment_return, name="payment_return"),
    
    # REFRESH JWT TOKEN API
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    # USER PATHS
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('my-events/', views.my_events, name='my_events'),
    path('user/', views.user_page, name='user_page'),
]