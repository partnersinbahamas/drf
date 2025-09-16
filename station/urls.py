from django.urls import path

from .views import BusListView, BusDetailView

app_name = 'station'

urlpatterns = [
    path('buses/', BusListView.as_view(), name='bus_list'),
    path('buses/<int:pk>/', BusDetailView.as_view(), name='bus_detail'),
]
