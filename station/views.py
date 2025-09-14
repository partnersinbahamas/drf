from rest_framework.generics import get_object_or_404
from django.http import JsonResponse
from .models import Bus
from .serializers import BusSerializer


def bus_list(request):
    if request.method == 'GET':
        buses = Bus.objects.all()
        buses_serializer = BusSerializer(buses, many=True)

        return JsonResponse(buses_serializer.data, safe=False, status=200)

    return None

def bus_detail(request, pk):
    if request.method == 'GET':
        bus = get_object_or_404(Bus, pk=pk)
        bus_serializer = BusSerializer(bus)

        return JsonResponse(bus_serializer.data, status=200)

    return None
