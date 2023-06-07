from django.urls import path
from .views import ProfileView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user-detail'

urlpatterns = [
    path('', ProfileView.as_view(), name='profile-authorized'),
    path('<slug:username>/' , ProfileView.as_view(), name='profile'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
