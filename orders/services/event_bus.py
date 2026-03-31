from orders.services.ticket_service import generate_qr_for_order
from orders.services.notification_service import notify_order_paid
from orders.services.order_service import increase_ticket_sold

class EventBus:
    @staticmethod
    def publish(event_name, payload):
        print(f"[EVENT] {event_name} triggered with {payload}")

        if event_name == "order_paid":
            order_id = payload["order_id"]

            increase_ticket_sold(order_id)
            generate_qr_for_order(order_id)
            notify_order_paid(order_id)