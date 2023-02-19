from django.urls import path
from plants import views

urlpatterns = [
    path(r"", views.ListPlantView.as_view(), name="plant-list"),
    path(r"create/", views.CreatePlantView.as_view(), name="plant-create"),
    path(r"update/<int:plant_pk>/", views.UpdatePlantView.as_view(), name="plant-update"),
    # path(r"delete/<int:plant_pk>/", ..., name='plant-delete'),
    path(r"api-details/<int:plant_pk>/", views.PlantApiInfoView.as_view(), name="plant-api-details"),
    path(r"<int:plant_pk>/chart/", views.PlantChartView.as_view(), name="plant-chart"),
    #  path(r"<int:plant_pk>/", ..., name='plant-detail'),
    path(r"<int:plant_pk>/sensors/create/", views.SensorCreateView.as_view(), name="create-sensor"),
    path(r"<int:plant_pk>/sensors/update/<int:sensor_pk>/", views.SensorUpdateView.as_view(), name="update-sensor"),
    # path(r"<int:plant_pk>/sensors/delete/<int:sensor_pk>/")
]
