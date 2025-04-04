from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.timezone import datetime
from django.views.generic import CreateView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from .models import Plant, PlantEntry, PlantImage, PlantState


from easy_plants.models import Plant, PlantImage
from easy_plants.forms import PlantForm


class EPView:
    """
    A simple mixin to add a title to a view
    """

    title = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context


class HomeView(TemplateView, EPView):
    title = "Home"
    template_name = "easy_plants/home.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["plants"] = Plant.objects.filter(archived=False)
        context_data["PLANT_STATES"] = PlantState.__members__
        context_data["title"] = self.title

        return context_data


class ArchiveView(TemplateView):
    title = "Archive"
    template_name = "easy_plants/home.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["plants"] = Plant.objects.filter(archived=True)
        context_data["PLANT_STATES"] = PlantState.__members__
        context_data["title"] = self.title

        return context_data


class PlantCreateView(CreateView):
    model = Plant
    form_class = PlantForm
    success_url = reverse_lazy("easy_plants:home")
    template_name = "easy_plants/add_plant.html"

    def form_valid(self, form):
        # first, we have to save plant instance ...
        result = super().form_valid(form)

        # in order to save the images to it
        images = form.cleaned_data["images"]
        for image in images:
            PlantImage.objects.create(image=image, date=datetime.now(), plant=form.instance)

        # now we can return the result
        return result


class PlantImageCreateView(CreateView):
    model = PlantImage
    fields = ["plant", "date", "image"]
    success_url = reverse_lazy("easy_plants:add-plant-image")
    template_name = "easy_plants/add_plant_image.html"


class PlantDetailView(DetailView):
    model = Plant
    template_name = "easy_plants/plant_detail.html"
    context_object_name = "plant"


class PlantUpdateView(UpdateView):
    model = Plant
    form_class = PlantForm
    success_url = reverse_lazy("easy_plants:home")
    template_name = "easy_plants/plant_update.html"

    def form_valid(self, form):
        images = form.cleaned_data["images"]

        # in order to save the images to it
        for image in images:
            PlantImage.objects.create(image=image, date=datetime.now(), plant=form.instance)

        return super().form_valid(form)


class PlantEntryUpdateView(UpdateView):
    model = PlantEntry
    fields = ["date", "text"]
    template_name = "easy_plants/update_plant_entry.html"
    context_object_name = "plant_entry"

    def get_success_url(self):
        return reverse_lazy("easy_plants:plant-detail", kwargs={"pk": self.object.plant_id})


class PlantEntryDeleteView(DeleteView):
    model = PlantEntry
    template_name = "easy_plants/delete_plant_entry.html"
    context_object_name = "plant_entry"

    def get_success_url(self):
        return reverse_lazy("easy_plants:plant-detail", kwargs={"pk": self.object.plant_id})


def add_plant_entry(request):
    plant_id = request.POST.get("plant-id")
    text = request.POST.get("plant-entry")

    plant = PlantEntry(text=text, date=datetime.now(), plant_id=plant_id)
    plant.save()

    return redirect("easy_plants:plant-detail", pk=plant_id)
