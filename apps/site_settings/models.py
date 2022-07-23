from django import forms
from django.db import models
# Create your models here.
from wagtail.admin.panels import FieldPanel, HelpPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting


@register_setting(icon="code")
class PageHTML(BaseSetting):
    header_html = models.TextField("Header HTML", blank=True)
    footer_html = models.TextField("Footer HTML", blank=True)

    panels = [
        FieldPanel("header_html", widget=forms.Textarea(attrs={"rows": 10})),
        HelpPanel(
            """
            Raw HTML added at the end of the HTML head on every page. Useful for Analytics
            snippets, meta content and social graph headers.
            """
        ),
        FieldPanel("footer_html", widget=forms.Textarea(attrs={"rows": 10})),
        HelpPanel(
            """
            Raw HTML added at the end of the HTML body on every page. Useful for additional
            JavaScript.
            """
        ),
    ]

    class Meta:
        verbose_name = "Page HTML"
