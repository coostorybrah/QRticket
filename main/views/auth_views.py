from django.http import JsonResponse
from django.db.models import Q

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout

import json

User = get_user_model()

# ĐĂNG KÝ
def api_signup(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    data = json.loads(request.body)

    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password")
    
    # Check dữ liệu
    if not username or not email or not password:
        return JsonResponse({"error": "Missing fields"}, status=400)

    if len(password) < 6:
        return JsonResponse({"error": "Password too short"}, status=400)

    # Check tồn tại
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already exists"}, status=400)

    # Tạo user
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
    )

    login(request, user)

    return JsonResponse({
        "success": True,
        "avatar": user.avatar.url if user.avatar else None,
        "username": user.username,
        "email": user.email,
        "message": "Đăng kí thành công!"
    })


# ĐĂNG NHẬP
def api_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    data = json.loads(request.body)

    identifier = data.get("username")       # Username hoặc email 
    password = data.get("password")

    # Đăng nhập bằng username hoặc email
    user_obj = User.objects.filter(Q(username=identifier) | Q(email=identifier)).first()

    if user_obj:
        user = authenticate(request, username=user_obj.username, password=password)

        if user:
            login(request, user)
            return JsonResponse({
                "success": True,
                "avatar": user.avatar.url if user.avatar else None,
                "username": user.username,
                "email": user.email,
                "message": "Đăng nhập thành công!"
            })

    return JsonResponse({"error": "Invalid credentials"}, status=401)

# KIỂM TRA LOGIN
def api_me(request):
    if not request.user.is_authenticated:
        return JsonResponse({"loggedIn": False})

    return JsonResponse({
        "loggedIn": True,
        "avatar": request.user.avatar.url if request.user.avatar else None,
        "username": request.user.username,
        "email": request.user.email
    })


# ĐĂNG XUẤT
def api_logout(request):
    logout(request)
    return JsonResponse({"success": True})