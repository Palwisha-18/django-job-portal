
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
    path(r'recruiter/create/', views.RecruiterProfileCreateView.as_view(), name='create-user'),
    path(r'recruiter/list/', views.RecruiterProfileListView.as_view(), name='list-user'),
    path(r'recruiter/details/', views.RecruiterDetailsManageView.as_view(), name='details-user'),
    path(r'recruiter/update/', views.RecruiterUpdateView.as_view(), name='update-user'),
    path(r'user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'user/profile/', views.UserRetrieveView.as_view(), name='view-user-profile'),
    path(r'user/password/reset/', views.UserChangePasswordView.as_view(), name='update-user-password'),
    path(r'company/create/', views.CompanyCreateView.as_view(), name='create-company'),
    path(r'company/list/', views.CompanyListView.as_view(), name='list-company'),
]
