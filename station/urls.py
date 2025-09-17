from django.urls import path

from .views import BusListAPIView, BusDetailAPIView

app_name = 'station'

urlpatterns = [
    path('buses/', BusListAPIView.as_view(), name='bus_list'),
    path('buses/<int:pk>/', BusDetailAPIView.as_view(), name='bus_detail'),
]
