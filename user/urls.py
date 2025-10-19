from django.urls import path
from .views import CreateUserAPIView, AuthUserView, ManageUserAPIView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'user'

urlpatterns = [
    path('register/', CreateUserAPIView.as_view(), name='create'),
    path('me/', ManageUserAPIView.as_view(), name="manage"),
    # path('login/', AuthUserView.as_view(), name="login-token"),

    # JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
