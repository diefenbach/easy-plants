from django.urls import path

from easy_plants.views import (
    PlantActiveView,
    PlantArchiveView,
    PlantCreateView,
    PlantDetailView,
    PlantImageCreateView,
    PlantUpdateView,
    PlantEntryUpdateView,
    PlantEntryDeleteView,
    add_plant_entry,
)

app_name = "easy_plants"

urlpatterns = [
    path("", PlantActiveView.as_view(), name="home"),
    path("archive", PlantArchiveView.as_view(), name="archive"),
    path("add-plant/", PlantCreateView.as_view(), name="add-plant"),
    path("plant/<int:pk>/update", PlantUpdateView.as_view(), name="update-plant"),
    path("plant/<int:plant_pk>/add-plant-image/", PlantImageCreateView.as_view(), name="add-plant-image"),
    path("add-plant-entry/", add_plant_entry, name="add-plant-entry"),
    path("plant/<int:pk>/", PlantDetailView.as_view(), name="plant-detail"),
    path("plant-entry/<int:pk>/update/", PlantEntryUpdateView.as_view(), name="update-plant-entry"),
    path("plant-entry/<int:pk>/delete/", PlantEntryDeleteView.as_view(), name="delete-plant-entry"),
]
