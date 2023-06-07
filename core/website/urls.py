from django.urls import path, include

app_name = "website"

urlpatterns = [
    path("v1/accounts/", include("website.api.v1.accounts.urls")),
    path("v1/user-detail/", include("website.api.v1.user_detail.urls")),
    path("v1/main-page/", include("website.api.v1.main_page.urls")),
    path("v1/search/", include("website.api.v1.search.urls")),
]