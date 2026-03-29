from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # pages
    path('', include('main.urls')),

    # APIs
    path('api/', include('users.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/events/', include('events.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)