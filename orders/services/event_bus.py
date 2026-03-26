from orders.services.ticket_service import generate_qr_for_order
from orders.services.notification_service import send_order_email

class EventBus:
    @staticmethod
    def publish(event_name, payload):
        print(f"[EVENT] {event_name} triggered with {payload}")

        if event_name == "order_paid":
            order_id = payload["order_id"]

            generate_qr_for_order(order_id)
            send_order_email(order_id)