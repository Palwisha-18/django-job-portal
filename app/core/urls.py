
"""
URL mappings for the user API.
"""
from core import views
from django.urls import path

app_name = 'core'

urlpatterns = [
    path(r'manage-users/', views.RecruiterProfileListCreateView.as_view(), name='manage-users'),
    path(r'token/', views.CreateTokenView.as_view(), name='token'),
    path(r'details/', views.RecruiterDetailsManageView.as_view(), name='details'),
    path(r'update/', views.RecruiterUpdateView.as_view(), name='update'),
]
