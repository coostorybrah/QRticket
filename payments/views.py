from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import Order
from payments.services.core import mark_order_paid

import json

@csrf_exempt
def paypal_webhook(request):
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"error": "invalid json"}, status=400)

    event_type = data.get("event_type")

    if event_type == "CHECKOUT.ORDER.APPROVED":
        resource = data.get("resource", {})
        paypal_id = resource.get("id")

        try:
            order = Order.objects.get(
                payment_id=paypal_id,
                payment_provider="paypal"
            )
        except Order.DoesNotExist:
            return JsonResponse({"error": "order not found"}, status=404)

        mark_order_paid(
            order,
            payment_id=paypal_id,
            provider="paypal"
        )

        print("✅ ORDER MARKED PAID:", order.id)

    return JsonResponse({"status": "ok"})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def find_order_by_paypal(request):
    paypal_id = request.GET.get("paypal_id")

    try:
        order = Order.objects.get(payment_id=paypal_id, user=request.user)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    return Response({
        "order_id": order.id
    })