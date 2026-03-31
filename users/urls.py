from django.urls import path
from users.views.auth_views import api_login, api_signup, api_me
from users.views.user_page_views import api_upload_avatar, api_update_username, api_change_password

urlpatterns = [
    # AUTH
    path("auth/login/", api_login),
    path("auth/signup/", api_signup),
    path("auth/me/", api_me),

    # USER PROFILE
    path("user/avatar/", api_upload_avatar),
    path("user/username/", api_update_username),
    path("user/password/", api_change_password),
]