from django.urls import path, include

from .views import BusViewSet, TripViewSet
from rest_framework import routers

app_name = 'station'

router = routers.DefaultRouter()
router.register('buses', BusViewSet, basename='buses')
router.register('trips', TripViewSet, basename='trips')

urlpatterns = [
    path('', include(router.urls))
]