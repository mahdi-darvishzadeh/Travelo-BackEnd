from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

"""Initial Url Patterns"""
api_urlpatterns = [path("api/", include("website.urls"))]

urlpatterns = [
    path("admin/", admin.site.urls),
]


"""Swagger Configurations"""
schema_view = get_schema_view(
    openapi.Info(
        title="APP API",
        default_version="v1",
        description="Change me Later",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

if settings.SHOW_SWAGGER:
    api_urlpatterns += [
        path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
        path(
            "swagger/api.json",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]


"""Additional configuration"""
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.SHOW_DEBUGGER_TOOLBAR:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

handler400 = "core.error_views.error_400"  # bad_request
handler403 = "core.error_views.error_403"  # permission_denied
handler404 = "core.error_views.error_404"  # page_not_found
handler500 = "core.error_views.error_500"  # server_error


"""Add api_urls"""
urlpatterns += api_urlpatterns
