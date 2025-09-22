from django.urls import path, include

from .views import BusViewSet, TripViewSet, FacilityViewSet, OrderViewSet
from rest_framework import routers

app_name = 'station'

router = routers.DefaultRouter()
router.register('buses', BusViewSet, basename='buses')
router.register('trips', TripViewSet, basename='trips')
router.register('facilities', FacilityViewSet, basename='facilities')
router.register('orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls))
]