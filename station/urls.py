from django.urls import path

from .views import BusListViewSet, BusDetailViewSet

app_name = 'station'

urlpatterns = [
    path(
        'buses/',
        BusListViewSet.as_view(
            actions={
                'get': 'list',
                'post': 'create'
            }
        ),
        name='bus_list'
    ),
    path(
        'buses/<int:pk>/',
        BusDetailViewSet.as_view(
            actions={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            }
        ),
        name='bus_detail'
    ),
]
