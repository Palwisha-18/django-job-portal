from core.models import (
    Recruiter,
    Company,
)
from core.permissions import (
    IsOwner
)
from core.serializers import (
    UserChangePasswordSerializer,
    CompanySerializer,
    RecruiterSerializer,
    RecruiterRetrieveListSerializer,
    UserSerializer
)
from rest_framework import permissions
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveDestroyAPIView,
    UpdateAPIView
)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_205_RESET_CONTENT
)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class UserRetrieveView(RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self):
        return self.request.user


class RecruiterProfileCreateView(CreateAPIView):
    """ Create Recruiter Instance """
    serializer_class = RecruiterSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class RecruiterProfileListView(ListAPIView):
    """ List Recruiter Instances"""
    serializer_class = RecruiterRetrieveListSerializer
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

        return Recruiter.objects.none()


class RecruiterDetailsManageView(RetrieveDestroyAPIView):
    """ Retrieve or Delete Recruiter Profile """
    serializer_class = RecruiterRetrieveListSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

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
    """ Update Recruiter Profile """
    serializer_class = RecruiterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.recruiter


class CompanyCreateView(CreateAPIView):
    """ Create Company Instance """
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class CompanyListView(ListAPIView):
    """ List all Company Instances """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]


class UserChangePasswordView(UpdateAPIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)
