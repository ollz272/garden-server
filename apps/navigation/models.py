from wagtail.admin.panels import MultiFieldPanel, StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.fields import StreamField

from navigation.blocks import LinksBlock


@register_setting(icon="list")
class HeaderLinks(BaseSetting):
    header_links = StreamField(
        LinksBlock(max_num=5, required=False),
        help_text="Shown to all users. A maximum of 5 can be added",
        blank=True,
    )

    logged_in_header_links = StreamField(
        LinksBlock(max_num=5, required=False),
        help_text=(
            "Only shown to logged in users. Standard header links will be shown if this list is "
            "empty. A maximum of 5 can be added."
        ),
        blank=True,
    )

    panels = [
        MultiFieldPanel(
            [
                StreamFieldPanel("header_links"),
                StreamFieldPanel("logged_in_header_links"),
            ],
            "Header Links",
        ),
    ]
