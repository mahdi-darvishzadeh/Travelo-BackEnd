from django.urls import path
from .views import *
from django.conf.urls.static import static
from .views import TripViewSet

app_name = "main-page"

urlpatterns = [
    path('' , TripViewSet.as_view({"get":"list"}), name='trip')  
]