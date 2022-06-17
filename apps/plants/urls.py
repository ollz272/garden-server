from django.urls import path
from plants import views

urlpatterns = [
    path(r"", views.ListPlantView.as_view(), name="plant-list"),
    path(r"create/", views.CreatePlantView.as_view(), name="plant-create"),
    path(r"update/<int:pk>/", views.UpdatePlantView.as_view(), name="plant-update"),
    path(r"api-details/<int:pk>/", views.PlantApiInfoView.as_view(), name="plant-api-details"),
    path(r"chart/<int:pk>/", views.PlantChartView.as_view(), name="plant-chart"),
]
