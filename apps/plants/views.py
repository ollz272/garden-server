from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormMixin, UpdateView
from plants.forms import PlantDataFilterForm, PlantForm, SensorForm
from plants.mixins import PlantViewMixin
from plants.models import Plant, Sensor


class CreatePlantView(LoginRequiredMixin, PlantViewMixin, CreateView):
    model = Plant
    form_class = PlantForm
    template_name = "plants/create.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("plant-chart", kwargs={"plant_pk": self.object.pk})


class UpdatePlantView(LoginRequiredMixin, PlantViewMixin, UpdateView):
    model = Plant
    form_class = PlantForm
    template_name = "plants/update.html"
    pk_url_kwarg = "plant_pk"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("plant-chart", kwargs={"plant_pk": self.object.pk})


class ListPlantView(LoginRequiredMixin, PlantViewMixin, ListView):
    model = Plant
    template_name = "plants/list.html"
    context_object_name = "plants"


class PlantChartView(LoginRequiredMixin, FormMixin, DetailView):
    model = Plant
    template_name = "plants/charts.html"
    form_class = PlantDataFilterForm
    pk_url_kwarg = "plant_pk"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()

        return super().get_queryset().filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["plant"] = self.object
        if data := self.request.GET:
            kwargs["data"] = data
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        if self.request.GET and form.is_valid():
            context["chart_data"] = form.chart_data()
        else:
            context["chart_data"] = self.object.to_chart_data()
        return context


class PlantApiInfoView(LoginRequiredMixin, PlantViewMixin, DetailView):
    """
    View to detail how to make various API requests.
    """

    model = Plant
    template_name = "plants/api_details.html"
    pk_url_kwarg = "plant_pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sensors"] = self.object.sensors.all()

        return context


class SensorCreateView(CreateView):
    model = Sensor
    form_class = SensorForm
    template_name = "plants/create_sensor.html"
    plant_url_kwarg = "plant_pk"

    def get_plant(self):
        plant_pk = self.kwargs.get(self.plant_url_kwarg)
        return get_object_or_404(Plant.objects.filter(user=self.request.user), pk=plant_pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["plant"] = self.get_plant()
        return kwargs

    def get(self, *args, **kwargs):
        self.plant = self.get_plant()
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.plant = self.get_plant()
        return super().post(*args, **kwargs)

    def get_success_url(self):
        return reverse("plant-chart", kwargs={"plant_pk": self.plant.pk})


class SensorUpdateView(UpdateView):
    model = Sensor
    form_class = SensorForm
    template_name = "plants/update_sensor.html"
    pk_url_kwarg = "sensor_pk"
    plant_url_kwarg = "plant_pk"
    context_object_name = "sensor"

    def get_queryset(self):
        return Sensor.objects.filter(plant=self.plant)

    def get_plant(self):
        plant_pk = self.kwargs.get(self.plant_url_kwarg)
        return get_object_or_404(Plant.objects.filter(user=self.request.user), pk=plant_pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["plant"] = self.get_plant()
        return kwargs

    def get(self, *args, **kwargs):
        self.plant = self.get_plant()
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.plant = self.get_plant()
        return super().post(*args, **kwargs)

    def get_success_url(self):
        return reverse("plant-chart", kwargs={"plant_pk": self.plant.pk})
