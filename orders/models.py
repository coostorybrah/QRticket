from django.db import models
from django.conf import settings

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    buyer_name = models.CharField(max_length=255, null=True, blank=True)
    buyer_email = models.EmailField(null=True, blank=True)
    buyer_phone = models.CharField(max_length=20, null=True, blank=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    ticket_type = models.ForeignKey("events.TicketType", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    qr_code = models.ImageField(upload_to="qrcodes/", null=True, blank=True)