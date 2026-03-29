from django.core.mail import send_mail
from orders.models import Order


def send_order_email(order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return

    email = order.buyer_email
    name = order.buyer_name

    send_mail(
        subject = "Your Ticket is Ready 🎫",
        message = f"Hello {name}\nYour order {order.id} has been successfully paid. Your QR tickets are ready.",
        from_email = "noreply@qrticket.com",
        recipient_list = [email],
        fail_silently = False,
    )

    print(f"[EMAIL] Sent to {email}")