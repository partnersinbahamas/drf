import pytest

from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient

from station.models import Bus
from station.serializers import BusListSerializer, BusSerializer
from station.tests.fixtures import get_user, get_admin, create_facility_wifi, create_facility_wc

BUS_DETAIL_PK = 1

BUS_LIST_URL = reverse_lazy("station:buses-list")
BUS_DETAIL_URL = reverse_lazy("station:buses-detail", args=[BUS_DETAIL_PK])

@pytest.fixture()
def create_bus(db):
    def index(**params):
        defaults = {
            "info": "AA 0000 BB",
            "num_seats": 50,
        }

        defaults.update(params)

        return Bus.objects.create(**defaults)

    return index


@pytest.fixture()
def create_buses_with_facilities(db, create_bus, create_facility_wifi, create_facility_wc):
    wifi_facility = create_facility_wifi
    wc_facility = create_facility_wc

    bus_1 = create_bus()
    bus_1.facilities.set([wifi_facility.id])
    bus_1.save()

    bus_2 = create_bus()
    bus_2.facilities.set([wc_facility.id])
    bus_2.save()

    return [bus_1, bus_2]


class TestPublicBusViewsSet:
    def setup_method(self):
        self.client = APIClient()

    # buses-list
    def test_bus_list_authentication_error(self):
        """ user does not authorize """

        response = self.client.get(BUS_LIST_URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        error_detail = response.data["detail"]
        assert error_detail == "Authentication credentials were not provided."
        assert error_detail.code == "not_authenticated"

    # buses-detail
    def test_bus_detail_authentication_error(self):
        """ user does not authorize """
        response = self.client.get(BUS_DETAIL_URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        error_detail = response.data["detail"]
        assert error_detail == "Authentication credentials were not provided."
        assert error_detail.code == "not_authenticated"


class TestPrivateBusViewsSet:
    def setup_method(self, get_user):
        self.client = APIClient()

    # buses-list
    def test_bus_list_authenticated_user_has_access(self, get_user, create_bus):
        """ user has access """
        bus = create_bus

        user = get_user
        self.client.force_authenticate(user)

        response = self.client.get(BUS_LIST_URL)
        buses = Bus.objects.all()
        bus_serializer = BusListSerializer(buses, many=True)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == bus_serializer.data


    def test_create_bus_forbidden(self, get_user):
        user = get_user
        self.client.force_authenticate(user)

        response = self.client.post(BUS_LIST_URL, {
            "info": "AA 0101 CC",
            "num_seats": 20,
        })

        error_detail = response.data["detail"]

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert error_detail == "You do not have permission to perform this action."
        assert error_detail.code == "permission_denied"


    def test_bus_list_should_be_filtered_by_facilities(self, get_user, create_buses_with_facilities):
        """ buses should be filtered by facilities """
        buses = create_buses_with_facilities

        user = get_user
        self.client.force_authenticate(user)

        response = self.client.get(BUS_LIST_URL, { "facilities": [1] })
        facilities_buses = Bus.objects.filter(facilities__in=[1])
        bus_serializer = BusListSerializer(facilities_buses, many=True)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == bus_serializer.data
        # buses[1] this is a bus with WC facility (id=2)
        assert buses[1] not in response.data


    def test_bus_should_be_created_by_admin(self, get_admin, create_facility_wifi):
        admin = get_admin
        wifi_facility = create_facility_wifi

        self.client.force_authenticate(admin)

        response = self.client.post(BUS_LIST_URL, {
            "info": "AA 0101 CC",
            "num_seats": 20,
            "facilities": [wifi_facility.id]
        })

        bus = Bus.objects.get(id=response.data["id"])
        bus_serializer = BusSerializer(bus)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == bus_serializer.data


    # buses-detail
    def test_bus_detail_authenticated_user_has_access(self, get_user, create_buses_with_facilities):
        """ user has access """
        buses = create_buses_with_facilities
        user = get_user
        self.client.force_authenticate(user)

        response = self.client.get(BUS_DETAIL_URL)

        bus_detail = Bus.objects.get(pk=BUS_DETAIL_PK)
        bus_serializer = BusListSerializer(bus_detail)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == bus_serializer.data


    def test_bus_detail_update_forbidden(self, get_user, create_buses_with_facilities):
        user = get_user
        self.client.force_authenticate(user)

        response = self.client.patch(BUS_DETAIL_URL, {
            "info": "AA 0101 CC",
        })

        error_detail = response.data["detail"]

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert error_detail == "You do not have permission to perform this action."
        assert error_detail.code == "permission_denied"
