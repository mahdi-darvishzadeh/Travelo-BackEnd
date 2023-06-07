from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from .views import TripSearchGenericAPIView

app_name = "search"

urlpatterns = [
    path('trip/' , TripSearchGenericAPIView.as_view(), name="partial-search")  
]