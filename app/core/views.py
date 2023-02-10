from core.models import Recruiter
from core.serializers import (
    RecruiterSerializer,
    RecruiterRetrieveListSerializer,
    AuthTokenSerializer,
)
from rest_framework import authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


class RecruiterProfileCreateView(ListCreateAPIView):
    serializer_class = RecruiterSerializer
    queryset = Recruiter.objects.all()


class RecruiterDetailsManageView(RetrieveUpdateDestroyAPIView):
    """Manage the authenticated user."""
    serializer_class = RecruiterRetrieveListSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user.recruiter

    def destroy(self, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.user.delete()
            return Response(data={'message': 'User Deleted Successfully'}, status=HTTP_200_OK)
        except Exception as e:
            return Response(data={'message': 'Operation Not Successful'}, status=HTTP_400_BAD_REQUEST)


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
