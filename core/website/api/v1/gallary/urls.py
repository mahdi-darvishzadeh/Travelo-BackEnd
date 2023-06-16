from django.urls import path
from .views import GallaryView,GallaryCreateAPIView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'gallary'

urlpatterns = [
    path('', GallaryView.as_view(), name='gallary'),
    path('create/', GallaryCreateAPIView.as_view(), name='create-gallary'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
