from django.urls import path
from .views import *
from django.conf.urls.static import static
from .views import TripViewSet,TripCreateAPIView

app_name = "main-page"

urlpatterns = [
    path('' , TripViewSet.as_view({"get":"list"}), name='trip'),
    path('trip/' , TripCreateAPIView.as_view(), name='create-trip'),  
]