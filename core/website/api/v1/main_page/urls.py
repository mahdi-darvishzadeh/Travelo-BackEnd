from django.urls import path
from .views import *
from django.conf.urls.static import static
from .views import TripViewSet

app_name = "main-page"

urlpatterns = [
    path('trip/' , TripViewSet.as_view({"get":"list"}), name='trip-list'),
    path('trip/<str:pk>/', TripViewSet.as_view({"get":"retrieve"}), name='trip-retrieve'),
]