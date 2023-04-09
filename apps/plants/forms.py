from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Div, Layout, Submit
from django import forms
from plants.choices import PeriodResolutionChoices
from plants.models import Plant, Sensor
from rest_framework.exceptions import ValidationError


class PlantDataFilterForm(forms.Form):
    """
    This form doesn't contain any actual logic - but helps to keep
    the peace re. layout & CSRF between Crispy Forms and django_filters.
    """

    start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))
    end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))
    resolution = forms.ChoiceField(choices=PeriodResolutionChoices.choices)

    def __init__(self, plant, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout("start_date", "end_date", "resolution")

        self.plant = plant
        if first_time := self.plant.plant_data.order_by("time").first():
            self.fields["start_date"].initial = first_time.time

        if last_time := self.plant.plant_data.order_by("-time").first():
            self.fields["end_date"].initial = last_time.time

    def clean(self):
        cleaned_date = super().clean()
        if cleaned_date["start_date"] > cleaned_date["end_date"]:
            self.add_error(None, ValidationError("Start date must come before end date."))
        return cleaned_date

    def chart_data(self):
        return self.plant.to_chart_data(
            time_from=self.cleaned_data["start_date"],
            time_to=self.cleaned_data["end_date"],
            resolution=self.cleaned_data["resolution"],
        )


class PlantForm(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "name",
            "indoor",
            ButtonHolder(Submit("save", "Save", css_class="submit")),
        )

    class Meta:
        model = Plant
        fields = (
            "name",
            "indoor",
        )

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.user:
            instance.user = self.user

        instance.save()
        return instance


class SensorForm(forms.ModelForm):
    def __init__(self, plant: Plant = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plant = plant
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div("name", css_class="col"),
            Div("unit", css_class="col"),
            Div("colour", css_class="col"),
            ButtonHolder(Submit("save", "Save", css_class="submit")),
        )

    class Meta:
        model = Sensor
        fields = ("name", "unit", "colour")
        widgets = {"colour": forms.TextInput(attrs={"type": "color"})}

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.plant:
            instance.plant = self.plant

        instance.save()
        return instance
