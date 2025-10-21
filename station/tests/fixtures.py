import pytest
from django.contrib.auth import get_user_model

from station.models import Facility


@pytest.fixture()
def get_user(db):
    return get_user_model().objects.create_user(
        username="Test user",
        password="user-password",
        email="user@example.com"
    )

@pytest.fixture()
def get_admin(db):
    return get_user_model().objects.create_user(
        username="Test admin",
        password="admin-password",
        email="admin@example.com",
        is_staff=True,
    )

@pytest.fixture()
def create_facility_wifi(db):
    return Facility.objects.create(name="wifi")

@pytest.fixture()
def create_facility_wc(db):
    return Facility.objects.create(name="wc")
