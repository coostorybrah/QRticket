from django.http import JsonResponse
from django.shortcuts import redirect
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import Order, OrderItem
from events.models import TicketType

from orders.services.event_bus import EventBus
from orders.services.payment_service import process_payment, cancel_order

from urllib.parse import urlencode
import datetime
import hashlib
import hmac

from django.urls import reverse
from django.http import JsonResponse

# PAYMENT
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_pay_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    if order.status == "PAID":
        return Response({"error": "Already paid"}, status=400)

    # MOCK MODE
    if not settings.VNPAY_ENABLED:
        mock_url = request.build_absolute_uri(
            f"/api/orders/payment-return/?vnp_ResponseCode=00&vnp_TxnRef={order.id}"
        )
        return Response({"payment_url": mock_url})

    # REAL VNPay (future)
    vnp_TmnCode = settings.VNPAY_TMN_CODE
    vnp_HashSecret = settings.VNPAY_HASH_SECRET
    vnp_Url = settings.VNPAY_URL
    return_url = settings.VNPAY_RETURN_URL

    amount = 100000

    vnp_Params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": vnp_TmnCode,
        "vnp_Amount": amount,
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": str(order.id),
        "vnp_OrderInfo": f"Thanh toan don hang {order.id}",
        "vnp_OrderType": "other",
        "vnp_Locale": "vn",
        "vnp_ReturnUrl": return_url,
        "vnp_IpAddr": "127.0.0.1",
        "vnp_CreateDate": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
    }

    sorted_params = sorted(vnp_Params.items())
    query_string = urlencode(sorted_params)

    hash_data = query_string.encode()
    secure_hash = hmac.new(
        vnp_HashSecret.encode(),
        hash_data,
        hashlib.sha512
    ).hexdigest()

    payment_url = f"{vnp_Url}?{query_string}&vnp_SecureHash={secure_hash}"

    return Response({"payment_url": payment_url})

# CREATE ORDER
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_create_order(request):

    if not request.data.get("buyer_name"):
        return Response({"error": "Missing name"}, status=400)

    if not request.data.get("buyer_email"):
        return Response({"error": "Missing email"}, status=400)

    if not request.data.get("buyer_phone"):
        return Response({"error": "Missing phone"}, status=400)

    order = Order.objects.create(
        user=request.user,
        buyer_name=request.data.get("buyer_name"),
        buyer_email=request.data.get("buyer_email"),
        buyer_phone=request.data.get("buyer_phone"),
    )

    return Response({
        "status": "success",
        "order_id": order.id
    })
    
# CANCEL ORDER
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

# DATA FOR USER'S BOUGHT TICKETS
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

# ADD ITEMS
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_add_items(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    items = request.data.get("items", [])

    for item in items:
        ticket = TicketType.objects.get(id=item["ticket_type_id"])

        OrderItem.objects.create(
            order=order,
            ticket_type=ticket,
            quantity=item["quantity"]
        )

    return Response({"status": "success"})

# VNPAY RESPONSE
@api_view(["GET"])
def payment_return(request):
    vnp_ResponseCode = request.GET.get("vnp_ResponseCode")
    order_id = request.GET.get("vnp_TxnRef")

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect("/")

    if vnp_ResponseCode == "00":
        order.status = "PAID"
        order.save()

        EventBus.publish("order_paid", {"order_id": order.id})

        return redirect("/my-tickets/")
    else:
        order.status = "CANCELLED"
        order.save()

        return redirect("/orders-failed/")