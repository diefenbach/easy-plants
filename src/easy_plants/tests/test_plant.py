import pytest

from django.utils import timezone


@pytest.mark.django_db
def test_flowering_day_and_week(plant):
    # One day
    plant.flowering_start = timezone.now() - timezone.timedelta(days=1)
    assert plant.get_flowering_day_and_week() == (1, 1)

    # Four days
    plant.flowering_start = timezone.now() - timezone.timedelta(days=4)
    assert plant.get_flowering_day_and_week() == (4, 1)

    # One week
    plant.flowering_start = timezone.now() - timezone.timedelta(weeks=1)
    assert plant.get_flowering_day_and_week() == (7, 1)

    # 10 days
    plant.flowering_start = timezone.now() - timezone.timedelta(days=10)
    assert plant.get_flowering_day_and_week() == (10, 2)

    # Two weeks
    plant.flowering_start = timezone.now() - timezone.timedelta(weeks=2)
    assert plant.get_flowering_day_and_week() == (14, 2)
