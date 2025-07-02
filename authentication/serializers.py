from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import CustomUser, DoctorProfile
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name','last_name', 'password1', 'password2']
    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError('Passwords do not match')
        return attrs
    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['email'],
            is_doctor=False
        )
        user.set_password(validated_data['password1'])
        user.save()


        return user


class DoctorSignUpSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(write_only=True)
    password2 =  serializers.CharField(write_only=True)


    class Meta:
        model =  CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def validate(self, data):
            if data['password1'] != data['password2']:
                raise serializers.ValidationError({"password": "Passwords do not match."})
            return data

    def create(self, validated_data):
            password = validated_data.pop('password1')
            validated_data.pop('password2')

            user = User.objects.create_user(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                email=validated_data['email'],
                username=validated_data['email'],
                is_doctor=True
            )

            user.set_password(password)
            user.save()

            return user

class DoctorSigninSerializer(serializers.Serializer):
            email = serializers.EmailField()
            password = serializers.CharField(write_only=True)

class DoctorProfileSerializer(serializers.ModelSerializer):
            class Meta:
                model = DoctorProfile
                fields = ['user', 'specialization', 'experience', 'contact_info', 'profile_picture']



