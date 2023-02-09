from core.serializers import RecruiterSerializer, AuthTokenSerializer
from rest_framework import authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView, )
from rest_framework.settings import api_settings


class RecruiterProfileCreateView(CreateAPIView):
    serializer_class = RecruiterSerializer


class RecruiterDetailsManageView(RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = RecruiterSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user.recruiter


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
