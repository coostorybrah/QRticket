import qrcode
from io import BytesIO
from django.core.files import File
from orders.models import OrderItem


def generate_qr_for_order(order_id):
    items = OrderItem.objects.filter(order_id=order_id)

    for item in items:
        data = f"ticket:{item.id}"

        qr = qrcode.make(data)

        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        filename = f"qr_{item.id}.png"
        item.qr_code.save(filename, File(buffer), save=True)