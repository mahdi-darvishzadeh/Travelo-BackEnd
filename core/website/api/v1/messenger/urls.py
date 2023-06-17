from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import MessageCreateAPIView, ChatCreateAPIView, MessangerViewSet

app_name = "messenger"

urlpatterns = [
    path('message', MessageCreateAPIView.as_view(), name='message'),
    path('chat', ChatCreateAPIView.as_view(), name='chat'),
    path('contacts' , MessangerViewSet.as_view({"get":"list"}), name='list-contacts'),
    path('retrieve/contact/<str:pk>/', MessangerViewSet.as_view({"get":"retrieve"}), name='retrieve-contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)