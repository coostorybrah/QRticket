from orders.models import Order
from .event_bus import EventBus

# PROCESS PAYMENT
def process_payment(order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return {"status": "error", "message": "Order not found"}

    # Prevent double payment
    if order.status == "PAID":
        return {"status": "error", "message": "Already paid"}

    # MOCK PAYMENT SUCCESS
    order.status = "PAID"
    order.save()

    # Trigger event
    EventBus.publish("order_paid", {"order_id": order.id})

    return {"status": "success", "order_id": order.id}

# CANCEL ORDER
def cancel_order(order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return {"status": "error", "message": "Order not found"}

    # Only allow cancel if not paid
    if order.status == "PAID":
        return {"status": "error", "message": "Cannot cancel a paid order"}

    if order.status == "CANCELLED":
        return {"status": "error", "message": "Already cancelled"}

    order.status = "CANCELLED"
    order.save()

    return {"status": "success", "order_id": order.id}