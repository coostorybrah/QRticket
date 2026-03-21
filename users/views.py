from django.http import JsonResponse

def api_upload_avatar(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    file = request.FILES.get("avatar")

    if not file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    if file.size > 2 * 1024 * 1024:
        return JsonResponse({"error": "File too large (max 2MB)"}, status=400)

    user = request.user

    if user.avatar:
        user.avatar.delete(save=False)

    user.avatar = file
    user.save()

    return JsonResponse({
        "success": True,
        "avatar": user.avatar.url
    })