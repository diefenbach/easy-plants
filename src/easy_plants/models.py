from math import ceil
from django.db import models
from django.utils import timezone
from enum import Enum
from django.urls import reverse


class PlantState(Enum):
    NOT_STARTED = 0
    STARTED = 1
    VEGETATIVE = 2
    FLOWERING = 3
    DRYING = 4
    FINISHED = 5


class Plant(models.Model):

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    start = models.DateField(blank=True, null=True)
    day_one = models.DateField(blank=True, null=True)
    flowering_start = models.DateField(blank=True, null=True)
    harvested = models.DateField(blank=True, null=True)
    drying_end = models.DateField(blank=True, null=True)
    archived = models.BooleanField(default=False)
    yield_wet = models.FloatField(blank=True, null=True)
    yield_dry = models.FloatField(blank=True, null=True)
    yield_kief = models.FloatField(blank=True, null=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_day_and_week(self):
        if not self.day_one:
            return 0, 0

        end_date = self.harvested or timezone.now().date()

        delta = end_date - self.day_one
        return delta.days, ceil(delta.days / 7)

    def get_flowering_day_and_week(self):
        if not self.flowering_start:
            return 0, 0

        flowering_end_date = self.harvested or timezone.now().date()

        delta = flowering_end_date - self.flowering_start

        delta_days = delta.days + 1

        return delta_days, ceil(delta_days / 7)

    def get_drying_day(self):
        if not self.harvested:
            return 0

        end_date = self.drying_end or timezone.now().date()
        delta = end_date - self.harvested

        return delta.days + 1

    def get_vegative_weeks(self):
        if not self.start or not self.day_one or not self.flowering_start:
            return 0

        delta = self.flowering_start - self.day_one

        return "%.1f" % (delta.days / 7)

    def get_state(self):
        if self.drying_end:
            return PlantState.FINISHED
        if self.harvested:
            return PlantState.DRYING
        if self.flowering_start:
            return PlantState.FLOWERING
        if self.day_one:
            return PlantState.VEGETATIVE
        if self.start:
            return PlantState.STARTED
        else:
            return None
        
    def get_absolute_url(self):
        return reverse("easy_plants:plant-detail", kwargs={"pk": self.id})


class PlantImage(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="images")
    date = models.DateField()
    image = models.ImageField(upload_to="plant_images")

    def __str__(self):
        return self.plant.name


class PlantEntry(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="entries")
    date = models.DateTimeField()
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.plant.name

    class Meta:
        ordering = ["-date"]

    @property
    def day(self):
        if not self.plant.day_one:
            return 0

        delta = self.date.date() - self.plant.day_one
        return delta.days + 1

    def get_absolute_url(self):
        return reverse("easy_plants:plant_entry_detail", kwargs={"pk": self.id})