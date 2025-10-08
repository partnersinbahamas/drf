from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, authentication
from rest_framework.settings import api_settings

from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken


class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserAPIView(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_object(self):
        return self.request.user


class AuthUserView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
