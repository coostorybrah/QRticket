from django.contrib import admin
from .models import Event, TicketType, Venue, Category

admin.site.register(Event)
admin.site.register(TicketType)
admin.site.register(Venue)
admin.site.register(Category)