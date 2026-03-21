from django.urls import path
from . import views

urlpatterns = [
    path("api/upload-avatar/", views.api_upload_avatar, name="upload_avatar"),

]