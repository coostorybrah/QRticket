from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from events.models import Event

# DATA TOAN BO SU KIEN
def api_events(request):
    events = Event.objects.filter(status="approved")

    data = {}

    for event in events:
        data[event.slug] = {
            "ten": event.name,
            "anh": event.image,
            "giaMin": float(event.min_price) if event.min_price else 0,
            "displayDate": event.date.strftime("%d.%m.%Y"),
            "startTime": event.start_time.strftime("%H:%M") if event.start_time else "",
            "endTime": event.end_time.strftime("%H:%M") if event.end_time else "",
            "categories": [c.slug for c in event.categories.all()]
        }

    return JsonResponse(data)

# DATA CHI TIET SU KIEN
def api_event_detail(request, event_id):
    event = get_object_or_404(Event, slug=event_id, status="approved")

    data = {
        "ten": event.name,
        "anh": event.image,
        "displayDate": event.date.strftime("%d.%m.%Y"),
        "startTime": event.start_time.strftime("%H:%M") if event.start_time else "",
        "endTime": event.end_time.strftime("%H:%M") if event.end_time else "",
        "dcTen": event.venue.name,
        "dcCuThe": f"{event.venue.address}, {event.venue.city}",
        "giaMin": float(event.min_price) if event.min_price else 0,
        "moTa": event.description,
        "tickets": [
            {
                "id": t.id,
                "loai": t.name,
                "gia": float(t.price)
            }
            for t in event.ticket_types.all()
        ]
    }

    return JsonResponse(data)