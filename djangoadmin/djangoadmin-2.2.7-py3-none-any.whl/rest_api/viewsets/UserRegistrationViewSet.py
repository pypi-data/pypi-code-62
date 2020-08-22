from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from djangoadmin.rest_api.serializers import UserRegistrationSerializer


class UserRegistrationViewSet(GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            data = {'username': instance.username, 'email': instance.email}
            return Response(data, status=201)
        return Response("Invalid data, Please try again!", status=401)