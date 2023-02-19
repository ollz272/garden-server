from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from apps.pages.blocks import HomePageStreamBlock


class BasePage(Page):
    """
    Just a placeholder for now incase I want to add any common page logic - not an abstract model incase we want to do
    any filtering on pages more generally!
    """

    subpage_types = []


class HomePage(BasePage):
    max_count = 1
    content = StreamField(HomePageStreamBlock, blank=True, use_json_field=True)

    content_panels = BasePage.content_panels + [FieldPanel("content")]

    subpage_types = ["BlogIndexPage", "StandardPage"]


class StandardPage(BasePage):
    content = StreamField(HomePageStreamBlock, blank=True, use_json_field=True)

    content_panels = BasePage.content_panels + [FieldPanel("content")]


class BlogIndexPage(BasePage):
    parent_page_types = ["pages.HomePage"]
    subpage_types = ["pages.BlogDetailPage"]


class BlogDetailPage(BasePage):
    parent_page_types = ["pages.BlogIndexPage"]

    abstract = models.TextField(blank=True)

    content = StreamField(HomePageStreamBlock, use_json_field=True)

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("abstract"),
            ],
            heading="Meta",
        ),
        FieldPanel("content"),
    ]
