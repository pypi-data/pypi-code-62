from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']