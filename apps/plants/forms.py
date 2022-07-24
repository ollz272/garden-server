from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Button, ButtonHolder, Div, Layout, Submit
from django import forms
from extra_views import InlineFormSetFactory
from plants.models import DataType, Plant


class PlantDataFilterForm(forms.Form):
    """
    This form doesn't contain any actual logic - but helps to keep
    the peace re. layout & CSRF between Crispy Forms and django_filters.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.add_input(Submit("submit", "Submit"))


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
