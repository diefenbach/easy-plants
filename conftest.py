import pytest

from easy_plants.models import Plant


@pytest.fixture
def plant():
    return Plant(name="Test Plant", type="Test Type")
