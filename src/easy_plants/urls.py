from django.urls import path

from easy_plants.views import (
    ArchiveView,
    HomeView,
    PlantCreateView,
    PlantDetailView,
    PlantImageCreateView,
    PlantUpdateView,
    add_plant_entry,
)

app_name = "easy_plants"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("archive", ArchiveView.as_view(), name="archive"),
    path("add-plant/", PlantCreateView.as_view(), name="add-plant"),
    path("plant/<int:pk>/update", PlantUpdateView.as_view(), name="update-plant"),
    path("plant/<int:plant_pk>/add-plant-image/", PlantImageCreateView.as_view(), name="add-plant-image"),
    path("add-plant-entry/", add_plant_entry, name="add-plant-entry"),
    path("plant/<int:pk>/", PlantDetailView.as_view(), name="plant-detail"),
]
