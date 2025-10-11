from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, authentication
from rest_framework.settings import api_settings

from app.serializers import CustomTokenAuthSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from user.serializers import UserSerializer


class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = []


class ManageUserAPIView(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_object(self):
        return self.request.user


class AuthUserView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = CustomTokenAuthSerializer
