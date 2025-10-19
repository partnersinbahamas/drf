import pytest
from django.contrib.auth import get_user_model


@pytest.fixture()
def get_user(db):
    return get_user_model().objects.create_user(
        username="Test user",
        password="user-password",
        email="user@example.com"
    )