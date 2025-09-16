from django.http import HttpRequest

from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Bus
from .serializers import BusSerializer

# function base api view
@api_view(['GET', 'POST'])
def bus_list(request):
    if request.method == 'GET':
        buses = Bus.objects.all()
        buses_serializer = BusSerializer(buses, many=True)

        return Response(buses_serializer.data, status=status.HTTP_200_OK)
    else:
        buses_serializer = BusSerializer(data=request.data)

        if buses_serializer.is_valid():
            buses_serializer.save()
        else:
            return Response(buses_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(buses_serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def bus_detail(request, pk):
    bus = get_object_or_404(Bus, pk=pk)

    if request.method == 'GET':
        bus_serializer = BusSerializer(bus)
        return Response(bus_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        bus_serializer = BusSerializer(bus, data=request.data)

        if bus_serializer.is_valid():
            bus_serializer.save()

            return Response(bus_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(bus_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        bus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class base api view
class BusListView(APIView):
    @staticmethod
    def get(request: HttpRequest) -> Response:
        buses = Bus.objects.all()
        serializer = BusSerializer(buses, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request: HttpRequest) -> Response:
        serializer = BusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BusDetailView(APIView):
    @staticmethod
    def get_object(pk: int) -> Bus:
        return get_object_or_404(Bus, pk=pk)

    def get(self, request: HttpRequest, pk: int) -> Response:
        bus = self.get_object(pk)
        serializer = BusSerializer(bus)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: HttpRequest, pk: int) -> Response:
        bus = self.get_object(pk)

        serializer = BusSerializer(bus, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: HttpRequest, pk: int) -> Response:
        bus = self.get_object(pk)

        serializer = BusSerializer(bus, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: HttpRequest, pk: int) -> Response:
        bus = self.get_object(pk)
        bus.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)