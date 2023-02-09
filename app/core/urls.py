
"""
URL mappings for the user API.
"""
from core import views
from django.urls import path

app_name = 'core'

urlpatterns = [
    path(r'create/', views.RecruiterProfileCreateView.as_view(), name='create'),
    path(r'token/', views.CreateTokenView.as_view(), name='token'),
    path(r'details/', views.RecruiterDetailsManageView.as_view(), name='details'),
]
