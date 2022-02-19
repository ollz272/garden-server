from rest_framework import routers

from apps.api.views import PlantViewSet, PlantDataViewSet

router = routers.SimpleRouter()
router.register(r'plant', PlantViewSet)
router.register(r'plant-data', PlantDataViewSet)

urlpatterns = router.urls
