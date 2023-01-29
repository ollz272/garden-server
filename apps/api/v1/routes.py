from api.v1.views import DataTypeViewSet, PlantDataViewSet, PlantViewSet
from rest_framework.routers import APIRootView, DefaultRouter

MODEL_PREFIX = "v1"
ROUTES = [
    ["plants", "v1-plants", PlantViewSet],
    ["plant-data-types", "v1-plant-data-types", DataTypeViewSet],
    ["plant-data", "v1-plant-data", PlantDataViewSet],
]


ROUTER_DOCSTRING = """
Garden Server - API - V1.0.0
=============================

This is our API for you to interact with the product on a programmatic basis.
"""


class V1APIRootView(APIRootView):
    __doc__ = ROUTER_DOCSTRING
    permission_classes = ()

    def get_view_name(self):
        return "Internal API Root"


class Router(DefaultRouter):
    APIRootView = V1APIRootView


def get_router_urls(routes=ROUTES):
    """
    Generate the routes so we can prevent namespace clashes on model names.
    Essentially we prefix the view-name with the app name.
    """
    router = Router()
    for prefix, base_name, viewset in routes:
        router.register(prefix, viewset, base_name)
    return router.get_urls()
