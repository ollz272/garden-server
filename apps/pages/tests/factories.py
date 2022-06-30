import wagtail_factories
import factory

from apps.pages.models import HomePage


class HomePageFactory(wagtail_factories.PageFactory):
    # required fields:
    title = "Home Page"

    class Meta:
        model = HomePage

