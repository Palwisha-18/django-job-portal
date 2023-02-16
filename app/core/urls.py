
"""
URL mappings for the user API.
"""
from core import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'core'

urlpatterns = [
    path(r'manage-users/', views.RecruiterProfileListCreateView.as_view(), name='manage-users'),
    path(r'details/', views.RecruiterDetailsManageView.as_view(), name='details'),
    path(r'update/', views.RecruiterUpdateView.as_view(), name='update'),
    path(r'token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
