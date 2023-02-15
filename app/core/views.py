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
    RetrieveDestroyAPIView,
    UpdateAPIView
)
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


class RecruiterProfileListCreateView(ListCreateAPIView):
    """ List or Create Users """
    serializer_class = RecruiterSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        is_super_user = getattr(self.request.user, 'is_superuser', None)
        if is_super_user:
            return Recruiter.objects.all()

        company = getattr(self.request.user.recruiter, 'company', None)
        is_admin = getattr(self.request.user.recruiter, 'is_admin', None)

        if not company or not is_admin:
            return Recruiter.objects.none()

        if is_admin:
            return Recruiter.objects.filter(company=company)

        return Recruiter.objects.all()


class RecruiterDetailsManageView(RetrieveDestroyAPIView):
    """ Retrieve or Delete User Profile """
    serializer_class = RecruiterRetrieveListSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.recruiter

    def destroy(self, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.user.delete()
            return Response(data={'message': 'User Deleted Successfully'}, status=HTTP_200_OK)
        except Exception as e:
            return Response(data={'message': 'Operation Not Successful'}, status=HTTP_400_BAD_REQUEST)


class RecruiterUpdateView(UpdateAPIView):
    """ Update User Profile"""

    serializer_class = RecruiterSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.recruiter


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
