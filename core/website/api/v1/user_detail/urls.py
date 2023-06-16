from django.urls import path
from .views import ProfileView, TripViewSet
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user-detail'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile-authorized'),
    path('profile/<slug:username>/' , ProfileView.as_view(), name='profile'),
    path('favorite/trip/' , TripViewSet.as_view({"get":"list"}), name='list-trip'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
