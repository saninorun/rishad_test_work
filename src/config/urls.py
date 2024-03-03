from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.goods.urls', namespace='catalog')),
    path('payments/', include('apps.payment.urls')),
    path('cart/', include('apps.carts.urls', namespace='carts')),
    # path('orders/', include('orders.urls', namespace='orders')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
