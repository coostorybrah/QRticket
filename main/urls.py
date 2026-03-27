from django.urls import path, include
from users.api_auth import login_jwt
from . import views

urlpatterns = [
    # MAIN PATHS
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("chitietsukien/<str:event_id>/", views.event_detail, name="event_detail"),
    path("orders/<str:event_id>/", views.orders_page, name="orders_page"),

    # USER PATHS
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('my-events/', views.my_events, name='my_events'),
    path('user/', views.user_page, name='user_page'),
    
    # EVENTS APIs
    path("api/events/", views.api_events, name="api_events"),
    path("api/events/<str:event_id>/", views.api_event_detail, name="api_event_detail"),
    
    # AUTHENTICATION APIs
    path("api/login/", views.api_login),
    path("api/token/", login_jwt),
    path("api/signup/", views.api_signup),
    path("api/me/", views.api_me),
    
    # ORDERS APIs
    path("api/orders/", include("orders.urls")),

]