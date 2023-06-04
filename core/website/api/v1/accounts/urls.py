from django.urls import path
from .views import (
    SignUpView, LoginView, UserNameView
)
from django.conf import settings

app_name = 'api-v1-accounts'

urlpatterns = [
    path('signup/' , SignUpView.as_view(), name='signup'),
    path('login/' , LoginView.as_view(), name='login'),
]
if settings.DEBUG:
    # Add additional URLs for debugging
    urlpatterns += [
            path("username/list/" , UserNameView.as_view(), name='get-username-list'),
    ]