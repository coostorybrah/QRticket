from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model
import uuid
import os

User = get_user_model()

# UPLOAD AVATAR
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_upload_avatar(request):
    user = request.user
    file = request.FILES.get("avatar")

    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    if not file.content_type.startswith("image/"):
        return Response({"error": "Invalid file type"}, status=400)

    if file.size > 2 * 1024 * 1024:
        return Response({"error": "File too large (max 2MB)"}, status=400)

    if user.avatar and user.avatar.name != "avatars/default-avatar.png":
        user.avatar.delete(save=False)

    ext = os.path.splitext(file.name)[1]
    file.name = f"{uuid.uuid4()}{ext}"

    user.avatar = file
    user.save()

    return Response({
        "success": True,
        "avatar": user.avatar.url
    })

# CHANGE USERNAME
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_update_username(request):
    user = request.user
    username = request.data.get("username", "").strip()

    if not username:
        return Response({"error": "Username cannot be empty"}, status=400)

    if User.objects.filter(username=username).exclude(id=user.id).exists():
        return Response({"error": "Username already taken"}, status=400)

    user.username = username
    user.save()

    return Response({"success": True})

# CHANGE PASSWORD
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_change_password(request):
    user = request.user

    current = request.data.get("current_password")
    new = request.data.get("new_password")
    confirm = request.data.get("confirm_password")

    if not user.check_password(current):
        return Response({"error": "Sai mật khẩu hiện tại"}, status=400)

    if new != confirm:
        return Response({"error": "Mật khẩu xác nhận không khớp"}, status=400)

    if len(new) < 6:
        return Response({"error": "Mật khẩu quá ngắn"}, status=400)

    user.set_password(new)
    user.save()

    return Response({"success": True})