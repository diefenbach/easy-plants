from django.contrib import admin
from .models import Plant, PlantEntry, PlantImage


class PlantAdmin(admin.ModelAdmin):
    list_display = ("name", "start", "day_one", "flowering_start", "harvested")
    search_fields = ("name",)
    list_filter = ("start", "day_one", "flowering_start", "harvested")


class PlantEntryAdmin(admin.ModelAdmin):
    list_display = ("plant", "date", "text")
    search_fields = ("plant__name", "text")
    list_filter = ("date",)


class PlantImageAdmin(admin.ModelAdmin):
    list_display = ("plant", "image")
    search_fields = ("plant__name",)


admin.site.register(Plant, PlantAdmin)
admin.site.register(PlantEntry, PlantEntryAdmin)
admin.site.register(PlantImage, PlantImageAdmin)
