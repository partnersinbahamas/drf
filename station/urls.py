from django.urls import path

from .views import BusViewSet

app_name = 'station'

bus_list_view = BusViewSet.as_view(actions={'get': 'list', 'post': 'create'})

bus_detail_view = BusViewSet.as_view(actions={
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path(
        'buses/',
        bus_list_view,
        name='bus_list'
    ),
    path(
        'buses/<int:pk>/',
        bus_detail_view,
        name='bus_detail'
    ),
]
