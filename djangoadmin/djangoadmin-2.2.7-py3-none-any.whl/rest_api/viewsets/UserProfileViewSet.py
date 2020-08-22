from rest_framework.generics import GenericAPIView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from djangoadmin.rest_api.serializers import UserProfileSerializer


class UserProfileViewSet(GenericAPIView):
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(User, username=self.request.user)
        data = {'id': instance.id, 'username': instance.username, 'email': instance.email}
        return Response(data, status=200)