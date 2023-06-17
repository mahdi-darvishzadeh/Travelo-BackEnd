from django.urls import path, include

app_name = "website"

urlpatterns = [
    path("v1/accounts/", include("website.api.v1.accounts.urls")),
    path("v1/user-detail/", include("website.api.v1.user_detail.urls")),
    path("v1/main-page/", include("website.api.v1.main_page.urls")),
    path("v1/search/", include("website.api.v1.search.urls")),
    path("v1/trip/", include("website.api.v1.trip.urls")),
    path("v1/add-to-favorite/", include("website.api.v1.add_to_favorite.urls")),
    path("v1/gallary/", include("website.api.v1.gallary.urls")),
    path("v1/messenger/", include("website.api.v1.messenger.urls")),
]