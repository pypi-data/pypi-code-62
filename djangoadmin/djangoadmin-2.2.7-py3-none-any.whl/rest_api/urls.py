from django.conf.urls import re_path
from djangoadmin.rest_api import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    re_path(r'^register/$', viewsets.UserRegistrationViewSet.as_view(), name='register_api'),
    re_path(r'^login/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
    re_path(r'^user/$', viewsets.UserProfileViewSet.as_view(), name='profile_api'),
]