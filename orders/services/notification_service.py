from django.core.mail import EmailMessage
from django.conf import settings

from orders.models import Order
from orders.services.pdf_service import generate_order_pdf


def notify_order_paid(order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        print("ORDER NOT FOUND", order_id)
        return
    
    print("NOTIFY START", order_id)
    pdf_buffer = generate_order_pdf(order)

    email = EmailMessage(
        subject="QRticket - Vé của bạn 🎫",
        body=f"Xin chào {order.buyer_name},\n\nVé của bạn được đính kèm trong file PDF.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[order.buyer_email],
    )

    email.attach(
        filename=f"tickets_order_{order.id}.pdf",
        content=pdf_buffer.getvalue(),
        mimetype="application/pdf"
    )

    try:
        email.send()
        print("EMAIL SENT")
    except Exception as e:
        print("EMAIL ERROR:", e)