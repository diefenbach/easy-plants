from django import forms
from .models import Plant


from easy_plants.models import Plant


# see https://docs.djangoproject.com/en/5.1/topics/class-based-views/generic-editing/#form-handling-with-class-based-views
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class DateInput(forms.DateInput):
    input_type = 'date'


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class PlantForm(forms.ModelForm):
    images = MultipleFileField(required=False)

    class Meta:
        model = Plant
        fields = [
            "name",
            "type",
            "start",
            "day_one",
            "flowering_start",
            "harvested",
            "drying_end",
            "yield_wet",
            "yield_dry",
            "yield_kief",
            "archived",
        ]
        widgets = {
            'start': DateInput(),
            'day_one': DateInput(),
            'flowering_start': DateInput(),
            'harvested': DateInput(),
            'drying_end': DateInput(),
        }
