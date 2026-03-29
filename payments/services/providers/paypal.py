
import requests
from django.conf import settings

from payments.services.core import mark_order_paid, mark_order_failed, validate_order_amount

# GET ACCESS TOKEN
def get_access_token():
    url = f"{settings.PAYPAL_BASE_URL}/v1/oauth2/token"

    response = requests.post(
        url,
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
        data={"grant_type": "client_credentials"}
    )

    data = response.json()
    return data["access_token"]

# CREATE ORDER
def create_order(order):
    access_token = get_access_token()

    url = f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    usd_total_price = convert_vnd_to_usd(order.get_total_price())
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "reference_id": str(order.id),
                "amount": {
                    "currency_code": "USD",
                    "value": f"{usd_total_price:.2f}",
                }
            }
        ],
        "application_context": {
            "return_url": f"https://{settings.BASE_URL}/payment-return/",
            "cancel_url": f"https://{settings.BASE_URL}/orders-failed/"
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    # store PayPal order ID
    paypal_id = data.get("id")
    order.payment_id = paypal_id
    order.payment_provider = "paypal"
    order.save()

    for link in data.get("links", []):
        if link["rel"] == "approve":
            return link["href"]

    return None

# WEBHOOK
def handle_webhook(data, order):
    """
    Simplified PayPal webhook handler (we’ll expand later)
    """

    status = data.get("status")
    amount = float(data.get("amount", 0))

    if order.status == "PAID":
        return {"status": "ignored"}

    if status != "COMPLETED":
        mark_order_failed(order)
        return {"status": "failed"}

    if not validate_order_amount(order, amount):
        return {"status": "invalid_amount"}

    mark_order_paid(
        order,
        payment_id = data.get("payment_id"),
        provider = "paypal"
    )

    return {"status": "success"}

def convert_vnd_to_usd(vnd_amount):
    rate  =  26000  # 1 USD ≈ 24,000 VND

    usd = vnd_amount / rate

    return round(usd, 2)