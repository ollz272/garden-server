from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from extra_views import (CreateWithInlinesView, NamedFormsetsMixin,
                         UpdateWithInlinesView)
from plants.forms import DataTypeFormHelper, DataTypeInline, PlantForm
from plants.mixins import PlantViewMixin
from plants.models import Plant


class CreatePlantView(LoginRequiredMixin, PlantViewMixin, CreateWithInlinesView, NamedFormsetsMixin):
    model = Plant
    form_class = PlantForm
    inlines = [DataTypeInline]
    inlines_names = ["datatypes_formset"]
    template_name = "plants/create.html"

    def forms_valid(self, form, inlines):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        for formset in inlines:
            formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["datatypes_formset_helper"] = DataTypeFormHelper()
        return context

    def get_success_url(self):
        return reverse("plant-chart", kwargs={"pk": self.object.pk})


class UpdatePlantView(LoginRequiredMixin, PlantViewMixin, UpdateWithInlinesView, NamedFormsetsMixin):
    model = Plant
    form_class = PlantForm
    inlines = [DataTypeInline]
    inlines_names = ["datatypes_formset"]
    template_name = "plants/update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["datatypes_formset_helper"] = DataTypeFormHelper()
        return context

    def get_success_url(self):
        return reverse("plant-chart", kwargs={"pk": self.object.pk})

    def forms_invalid(self, form, inlines):
        return super().forms_invalid(form, inlines)


class ListPlantView(LoginRequiredMixin, PlantViewMixin, ListView):
    model = Plant
    template_name = "plants/list.html"
    context_object_name = "plants"


class PlantChartView(LoginRequiredMixin, PlantViewMixin, DetailView):
    model = Plant
    template_name = "plants/charts.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()

        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chart_data"] = self.object.to_chart_data()
        return context


class PlantApiInfoView(LoginRequiredMixin, PlantViewMixin, DetailView):
    """
    View to detail how to make various API requests.
    """

    model = Plant
    template_name = "plants/api_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data_types"] = self.object.data_types.all()

        return context
