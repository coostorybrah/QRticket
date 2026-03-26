from django.http import JsonResponse
from orders.services.payment_service import process_payment, cancel_order
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import Order

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_pay_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    # AUTH CHECK (IMPORTANT)
    if order.user != request.user:
        return Response({"error": "Forbidden"}, status=403)

    result = process_payment(order_id)
    return Response(result)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_cancel_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    # AUTH CHECK
    if order.user != request.user:
        return Response({"error": "Forbidden"}, status=403)

    result = cancel_order(order_id)
    return Response(result)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_create_order(request):
    order = Order.objects.create(user=request.user)

    return Response({
        "status": "success",
        "order_id": order.id
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_my_tickets(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")

    data = []

    for order in orders:
        for item in order.items.all():
            data.append({
                "order_id": order.id,
                "ticket_type": item.ticket_type.name,
                "quantity": item.quantity,
                "qr_code": item.qr_code.url if item.qr_code else None
            })

    return Response(data)