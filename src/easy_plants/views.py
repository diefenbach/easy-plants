from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.timezone import datetime
from django.views.generic import CreateView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView

from easy_plants.models import Plant, PlantEntry, PlantImage, PlantState
from easy_plants.forms import PlantForm


class PlantActiveView(LoginRequiredMixin, TemplateView):
    """
    A view to display the active plants.
    """
    title = "Home"
    template_name = "easy_plants/plant_list.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["plants"] = Plant.objects.filter(archived=False)
        context_data["PLANT_STATES"] = PlantState.__members__
        context_data["title"] = self.title

        return context_data


class PlantArchiveView(LoginRequiredMixin, TemplateView):
    """
    A view to display the archived plants.
    """
    title = "Archive"
    template_name = "easy_plants/plant_list.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["plants"] = Plant.objects.filter(archived=True).order_by("-harvested")
        context_data["PLANT_STATES"] = PlantState.__members__
        context_data["title"] = self.title

        return context_data


class PlantCreateView(LoginRequiredMixin, CreateView):
    model = Plant
    form_class = PlantForm
    success_url = reverse_lazy("easy_plants:home")
    template_name = "easy_plants/plant_add.html"

    def form_valid(self, form):
        # first, we have to save plant instance ...
        result = super().form_valid(form)

        # in order to save the images to it
        images = form.cleaned_data["images"]
        for image in images:
            PlantImage.objects.create(image=image, date=datetime.now(), plant=form.instance)

        # now we can return the result
        return result


class PlantImageCreateView(LoginRequiredMixin, CreateView):
    model = PlantImage
    fields = ["plant", "date", "image"]
    success_url = reverse_lazy("easy_plants:add-plant-image")
    template_name = "easy_plants/add_plant_image.html"


class PlantDetailView(LoginRequiredMixin, DetailView):
    model = Plant
    template_name = "easy_plants/plant_detail.html"
    context_object_name = "plant"


class PlantUpdateView(LoginRequiredMixin, UpdateView):
    """
    A view to update a plant.
    """
    model = Plant
    form_class = PlantForm
    success_url = reverse_lazy("easy_plants:home")
    template_name = "easy_plants/plant_update.html"

    def form_valid(self, form):
        images = form.cleaned_data["images"]

        for image in images:
            PlantImage.objects.create(image=image, date=datetime.now(), plant=form.instance)

        return super().form_valid(form)


class PlantEntryUpdateView(LoginRequiredMixin, UpdateView):
    """
    A view to update a plant entry.
    """
    model = PlantEntry
    fields = ["date", "text"]
    template_name = "easy_plants/plant_entry_update.html"
    context_object_name = "plant_entry"

    def get_success_url(self):
        return reverse_lazy("easy_plants:plant-detail", kwargs={"pk": self.object.plant_id})


class PlantEntryDeleteView(LoginRequiredMixin, DeleteView):
    """
    A view to delete a plant entry.
    """
    model = PlantEntry
    template_name = "easy_plants/plant_entry_delete.html"
    context_object_name = "plant_entry"

    def get_success_url(self):
        return reverse_lazy("easy_plants:plant-detail", kwargs={"pk": self.object.plant_id})


@login_required
def add_plant_entry(request):
    plant_id = request.POST.get("plant-id")
    text = request.POST.get("plant-entry")

    plant = PlantEntry(text=text, date=datetime.now(), plant_id=plant_id)
    plant.save()

    return redirect("easy_plants:plant-detail", pk=plant_id)
