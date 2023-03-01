from core.error_messages import (
    MISSING_USER_MSG,
    USER_ALREADY_EXISTS_MSG,
)
from core.models import (
    Recruiter,
    Company,
)
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the user object """

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'role']
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


class UserChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def validate(self, data):
        if not data.get('password'):
            raise serializers.ValidationError({'message': 'Password field is required.'})

        return data

    def update(self, instance, validated_data):
        """ Update password of user """
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    @property
    def data(self):
        return {'message': 'Your password has been successfully updated!'}


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
        if not user_info:
            raise serializers.ValidationError(detail=USER_ALREADY_EXISTS_MSG, status_code=MISSING_USER_MSG)

        if get_user_model().objects.filter(email=user_info.get('email')).exists():
            raise serializers.ValidationError(detail=USER_ALREADY_EXISTS_MSG, status_code=HTTP_400_BAD_REQUEST)

        user = get_user_model().objects.create_user(**user_info)
        recruiter = Recruiter.objects.create(user=user, **validated_data)

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
