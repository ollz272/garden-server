from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Button, ButtonHolder, Div, Layout, Submit
from django import forms
from django.forms import SelectDateWidget
from django_filters.fields import DateTimeRangeField
from django_filters.widgets import RangeWidget
from extra_views import InlineFormSetFactory
from psycopg2._range import DateTimeTZRange
from rest_framework.exceptions import ValidationError

from plants.models import DataType, Plant


class PlantDataFilterForm(forms.Form):
    """
    This form doesn't contain any actual logic - but helps to keep
    the peace re. layout & CSRF between Crispy Forms and django_filters.
    """
    start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))
    end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))

    def __init__(self, plant, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "start_date",
            "end_date",
        )

        self.plant = plant
        if first_time := self.plant.plant_data.order_by('time').first():
            self.fields['start_date'].initial = first_time.time

        if last_time := self.plant.plant_data.order_by('-time').first():
            self.fields['end_date'].initial = last_time.time

    def clean(self):
        cleaned_date = super().clean()
        if cleaned_date['start_date'] > cleaned_date['end_date']:
            self.add_error(None, ValidationError("Start date must come before end date."))
        return cleaned_date

    def chart_data(self):
        return self.plant.to_chart_data(
            time_from=self.cleaned_data['start_date'],
            time_to=self.cleaned_data['end_date'],
        )

    class Meta:
        model = Plant
        fields = ("start_date", "end_date")


class DataTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                "id",
                Div("name", css_class="col"),
                Div("unit", css_class="col"),
                Div("colour", css_class="col"),
                css_class="row",
            ),
        )

    class Meta:
        model = DataType
        fields = ("name", "unit", "colour")
        widgets = {
            "id": forms.HiddenInput,
            "colour": forms.TextInput(attrs={"type": "color"})
        }


class DataTypeFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        self.render_hidden_fields = True


class DataTypeInline(InlineFormSetFactory):
    form_class = DataTypeForm
    model = DataType
    factory_kwargs = {
        "extra": 0,
        "validate_min": True,
        "can_delete": True,
        "validate_max": True,
        "max_num": 4,
        "min_num": 1,
    }


class PlantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.render_hidden_fields = True
        self.helper.layout = Layout(
            "name",
            "indoor",
            Div(
                HTML('{% include "plants/includes/datatype_formset.html" %}'),
                css_class="form",
            ),
            ButtonHolder(Submit("save", "Save", css_class="submit")),
        )

    class Meta:
        model = Plant
        fields = (
            "name",
            "indoor",
        )
