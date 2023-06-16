from django.urls import path
from .views import AddToFavoriteView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'add-to-favorite'

urlpatterns = [
    path('trip/<str:pk>/', AddToFavoriteView.as_view(), name='add-to-favorite'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
