from navigation.blocks import LinksBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.fields import StreamField


@register_setting(icon="list")
class HeaderLinks(BaseSetting):
    header_links = StreamField(
        LinksBlock(max_num=5, required=False),
        help_text="Shown to all users. A maximum of 5 can be added",
        blank=True,
        use_json_field=True,
    )

    logged_in_header_links = StreamField(
        LinksBlock(max_num=5, required=False),
        help_text=(
            "Only shown to logged in users. Standard header links will be shown if this list is "
            "empty. A maximum of 5 can be added."
        ),
        blank=True,
        use_json_field=True,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("header_links"),
                FieldPanel("logged_in_header_links"),
            ],
            "Header Links",
        ),
    ]
