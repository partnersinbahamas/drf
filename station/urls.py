from django.urls import path, include

from .views import BusViewSet
from rest_framework import routers

app_name = 'station'

router = routers.DefaultRouter()
router.register('buses', BusViewSet, basename='buses')

urlpatterns = [
    path('', include(router.urls))
]