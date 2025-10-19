import pytest

from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient

from station.models import Bus
from station.serializers import BusSerializer
from station.tests.fixtures import get_user


BUS_LIST_URL = reverse_lazy("station:buses-list")

@pytest.fixture()
def create_bus(db):
    defaults = {
        "info": "AA 0000 BB",
        "num_seats": 50,
    }

    return Bus.objects.create(**defaults)

class TestPublicBusViewsSet:
    def setup_method(self):
        self.client = APIClient()

    def test_api_authentication_error(self):
        """ user does not authorize """

        response = self.client.get(BUS_LIST_URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        error_detail = response.data["detail"]
        assert error_detail == "Authentication credentials were not provided."
        assert error_detail.code == "not_authenticated"


class TestPrivateBusViewsSet:
    def setup_method(self, get_user):
        self.client = APIClient()

    def test_authenticated_user_has_access(self, get_user, create_bus):
        """ user has access """

        user = get_user
        self.client.force_authenticate(user)

        bus = create_bus

        response = self.client.get(BUS_LIST_URL)
        buses = Bus.objects.all()
        bus_serializer = BusSerializer(buses, many=True)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == bus_serializer.data
