from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from orders.models import Order, OrderItem
from events.models import TicketType

from payments.services.manager import create_payment

# CREATE ORDER
def create_order(user, buyer_name, buyer_email, buyer_phone):
    if not buyer_name:
        return None, "Missing name"
    
    if not buyer_email:
        return None, "Missing email"

    if not buyer_phone:
        return None, "Missing phone"

    order = Order.objects.create(
        user=user,
        buyer_name=buyer_name,
        buyer_email=buyer_email,
        buyer_phone=buyer_phone,
        status="PENDING"
    )

    return order, None


# ADD ITEMS
def add_items(order, items):
    if order.status != "PENDING":
        return "Cannot modify order"

    with transaction.atomic():
        OrderItem.objects.filter(order=order).delete()

        for item in items:
            ticket_id = item.get("ticket_type_id")
            quantity = item.get("quantity")

            if not ticket_id or not quantity:
                return "Invalid item data"

            if quantity <= 0:
                return "Invalid quantity"

            ticket = get_object_or_404(TicketType, id=ticket_id)

            OrderItem.objects.create(
                order=order,
                ticket_type=ticket,
                quantity=quantity
            )

    return None

# PAY ORDER
def pay_order(order, provider="paypal"):
    if order.status == "PAID":
        return None, "Already paid"

    payment_url = create_payment(order, provider)

    if not payment_url:
        return None, "Payment creation failed"

    return payment_url, None

# CANCEL ORDER
def cancel_order(order):
    if order.status == "PAID":
        return "Cannot cancel paid order"

    if order.status == "CANCELLED":
        return "Already cancelled"

    order.status = "CANCELLED"
    order.save()

    return None

# UPDATE TICKET SOLD
@transaction.atomic
def increase_ticket_sold(order_id):
    order = Order.objects.get(id=order_id)

    for item in order.items.select_related("ticket_type"):
        ticket_type = item.ticket_type
        ticket_type.quantity_sold += item.quantity
        ticket_type.save(update_fields=["quantity_sold"])
        
# VALIDATE TICKET STOCK
def validate_ticket_stock(ticket_type, quantity):
    if quantity > ticket_type.quantity_available:
        raise ValidationError(
            f"Only {ticket_type.quantity_available} tickets left for {ticket_type.name}"
        )