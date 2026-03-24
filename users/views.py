from django.http import JsonResponse
from django.contrib.auth import get_user_model, update_session_auth_hash

import json
import uuid
import os

# UPLOAD AVATAR
def api_upload_avatar(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    file = request.FILES.get("avatar")

    if not file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    if not file.content_type.startswith("image/"):
        return JsonResponse({"error": "Invalid file type"}, status=400)

    if file.size > 2 * 1024 * 1024:
        return JsonResponse({"error": "File too large (max 2MB)"}, status=400)

    user = request.user

    if user.avatar and user.avatar.name != "avatars/default-avatar.png":
        user.avatar.delete(save=False)

    ext = os.path.splitext(file.name)[1]
    file.name = f"{uuid.uuid4()}{ext}"
    
    user.avatar = file
    user.save()

    return JsonResponse({
        "success": True,
        "avatar": user.avatar.url
    })
    


User = get_user_model()

# CHANGE USERNAME
def api_update_username(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    data = json.loads(request.body)
    username = data.get("username", "").strip()

    if not username:
        return JsonResponse({"error": "Username cannot be empty"})

    if User.objects.filter(username=username).exclude(id=request.user.id).exists():
        return JsonResponse({"error": "Username already taken"})

    request.user.username = username
    request.user.save()

    return JsonResponse({"success": True})

# CHANGE PASSWORD
def api_change_password(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    data = json.loads(request.body)

    current = data.get("current_password")
    new = data.get("new_password")
    confirm = data.get("confirm_password")

    if not request.user.check_password(current):
        return JsonResponse({"error": "Sai mật khẩu hiện tại"})

    if new != confirm:
        return JsonResponse({"error": "Mật khẩu xác nhận không khớp"})

    if len(new) < 6:
        return JsonResponse({"error": "Mật khẩu quá ngắn"})

    request.user.set_password(new)
    request.user.save()

    update_session_auth_hash(request, request.user)

    return JsonResponse({"success": True})