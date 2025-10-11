from django.db.models import Prefetch
from django.http import HttpRequest

from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets
from rest_framework.views import APIView

from .models import Bus, Trip, Facility, Order, Ticket
from .permissions import IsAdminOrIsAuthenticated
from .paginations import OrderListPagination
from .serializers import BusSerializer, TripSerializer, TripListSerializer, TripRetrieveSerializer, BusListSerializer, \
    FacilitySerializer, OrderSerializer, OrderListSerializer


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


# generic base api view
class BusListAPIView(generics.ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

    # use to add an additional login for a method. Starts with prefix perform_*
    # def perform_create(self, serializer):
    #     pass


class BusDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer


# viewset base api view
class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all().prefetch_related('facilities')
    serializer_class = BusSerializer

    _actions_list = ['list', 'retrieve']

    @staticmethod
    def param_from_query(query_params: str | None):
        return [int(param.strip()) for param in query_params.split(',')]

    def get_queryset(self):
        queryset = self.queryset
        facilities_query = self.request.query_params.get('facilities', None)

        if facilities_query:
            facilities_params = self.param_from_query(facilities_query)
            queryset = queryset.filter(facilities__in=facilities_params).distinct()

        return queryset

    def get_serializer_class(self):
        if self.action in self._actions_list:
            return BusListSerializer

        return BusSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = (
        Trip.objects
            .select_related('bus')
            .prefetch_related(
                'tickets',
                Prefetch('bus__facilities', queryset=Facility.objects.all())
            )
    )

    def get_serializer_class(self):
        if self.action == 'list':
            return TripListSerializer
        elif self.action == 'retrieve':
            return TripRetrieveSerializer

        return TripSerializer


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer


class OrderViewSet(viewsets.ModelViewSet):
    pagination_class = OrderListPagination
    queryset = Order.objects.prefetch_related(
        Prefetch('tickets',
            queryset=Ticket.objects
                 .select_related('trip__bus')
                 .prefetch_related('trip__tickets')
        )
    )

    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.request.user.is_authenticated:
            return queryset.filter(user_id=self.request.user.id)
        return queryset.none()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return OrderListSerializer

        return OrderSerializer


    def perform_create(self, serializer):
        return serializer.save(user_id=self.request.user.id)
