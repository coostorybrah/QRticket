from django.core.mail import send_mail
from orders.models import Order


def send_order_email(order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return

    user_email = order.user.email

    send_mail(
        subject="Your Ticket is Ready 🎫",
        message=f"Your order {order.id} has been successfully paid. Your QR tickets are ready.",
        from_email="noreply@qrticket.com",
        recipient_list=[user_email],
        fail_silently=True,
    )

    print(f"[EMAIL] Sent to {user_email}")