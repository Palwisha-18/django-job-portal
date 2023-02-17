
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
    path(r'user/create/', views.RecruiterProfileCreateView.as_view(), name='create-user'),
    path(r'user/list/', views.RecruiterProfileListView.as_view(), name='list-user'),
    path(r'user/details/', views.RecruiterDetailsManageView.as_view(), name='details-user'),
    path(r'user/update/', views.RecruiterUpdateView.as_view(), name='update-user'),
    path(r'user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'company/create/', views.CompanyCreateView.as_view(), name='create-company'),
    path(r'company/list/', views.CompanyListView.as_view(), name='list-company'),
]
