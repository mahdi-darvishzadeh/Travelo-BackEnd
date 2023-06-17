from django.urls import path
from .views import VoteAPIView
from django.conf.urls.static import static
from .views import VoteAPIView, TripCreateAPIView

app_name = "trip"

urlpatterns = [
    path('' , TripCreateAPIView.as_view(), name='create-trip'),  
    path('<str:pk>/vote/' , VoteAPIView.as_view(), name='vote-trip'),  
]