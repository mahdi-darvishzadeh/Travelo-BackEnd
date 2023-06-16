from django.urls import path
from .views import ProfileView, FavoriteTripViewSet, MyTripViewSet,PeopleViewSet
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user-detail'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile-authorized'),
    path('profile/<slug:username>/' , ProfileView.as_view(), name='profile'),
    path('favorite/trip/' , FavoriteTripViewSet.as_view({"get":"list"}), name='list-favorite-trip'),
    path('mytrip/' , MyTripViewSet.as_view({"get":"list"}), name='list-my-trip'),
    path('people/' , PeopleViewSet.as_view({"get":"list"}), name='list-people'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
