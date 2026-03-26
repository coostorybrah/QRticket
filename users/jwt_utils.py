from rest_framework_simplejwt.authentication import JWTAuthentication

def get_user_from_request(request):
    jwt_auth = JWTAuthentication()

    try:
        user_auth_tuple = jwt_auth.authenticate(request)
        if user_auth_tuple is not None:
            user, token = user_auth_tuple
            return user
    except:
        return None

    return None