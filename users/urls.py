from django.urls import path
from . import views

urlpatterns = [
    path("api/upload-avatar/", views.api_upload_avatar, name="upload_avatar"),
    path("api/update-username/", views.api_update_username),
    path("api/change-password/", views.api_change_password),
]