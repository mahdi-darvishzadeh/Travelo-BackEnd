from django.urls import path
from .views import ProfileView

app_name = 'user-detail'

urlpatterns = [
    path('', ProfileView.as_view(), name='profile-authorized'),
    path('<slug:username>/' , ProfileView.as_view(), name='profile'),
]