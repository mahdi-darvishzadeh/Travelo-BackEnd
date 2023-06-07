from django.urls import path
from .views import *
from django.conf.urls.static import static
from .views import VoteAPIView

app_name = "trip"

urlpatterns = [
    path('<str:pk>/vote/' , VoteAPIView.as_view(), name='trip'),  
]