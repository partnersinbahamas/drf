from django.urls import path
from .views import CreateUserAPIView, AuthUserView, ManageUserAPIView

app_name = 'user'

urlpatterns = [
    path('register/', CreateUserAPIView.as_view(), name='create'),
    path('me/', ManageUserAPIView.as_view(), name="manage"),
    path('login/', AuthUserView.as_view(), name="login-token"),
]
