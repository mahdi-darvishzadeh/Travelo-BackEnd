from django.urls import path
from .views import AddToFavoriteView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'gallary'

urlpatterns = [
    path('', AddToFavoriteView.as_view(), name='gallary'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
