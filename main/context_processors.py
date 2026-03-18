def current_user(request):
    if request.user.is_authenticated:
        return {"user": request.user}
    return {"user": None}