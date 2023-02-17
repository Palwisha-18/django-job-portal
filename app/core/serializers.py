from core.models import Recruiter, Company
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the user object """

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """ Create and return a user with encrypted password """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """ Update and return user """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class CompanySerializer(serializers.ModelSerializer):
    """ Serializer for the company object """
    class Meta:
        model = Company
        fields = '__all__'


class RecruiterSerializer(serializers.ModelSerializer):
    """ Serializer for the recruiter object """
    user = UserSerializer()

    class Meta:
        model = Recruiter
        fields = '__all__'

    def create(self, validated_data):
        user_info = validated_data.pop('user', None)
        if user_info:
            if get_user_model().objects.filter(email=user_info.get('email')).exists():
                res = serializers.ValidationError()
                res.status_code = HTTP_400_BAD_REQUEST
                res.detail = {
                    'message': 'A user with this email already exists!',
                    'user_exists_error': True
                }
                raise res
            user = get_user_model().objects.create_user(**user_info)
            recruiter = Recruiter.objects.create(user=user, **validated_data)
        else:
            res = serializers.ValidationError()
            res.status_code = HTTP_400_BAD_REQUEST
            res.detail = {
                'message': 'User object is missing from request.',
                'missing_user_object': True
            }
            raise res

        return recruiter

    def update(self, instance, validated_data):
        user_info = validated_data.pop("user", None)
        if user_info:
            UserSerializer(data=user_info).update(instance.user, user_info)

        super().update(instance, validated_data)
        return instance


class RecruiterRetrieveListSerializer(serializers.ModelSerializer):
    """ Serializer for the recruiter object """
    user = UserSerializer()
    company = CompanySerializer()

    class Meta:
        model = Recruiter
        fields = '__all__'
