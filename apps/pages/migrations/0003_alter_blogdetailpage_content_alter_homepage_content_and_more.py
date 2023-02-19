# Generated by Django 4.1.5 on 2023-01-29 13:37

import wagtail.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0002_create_homepage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogdetailpage",
            name="content",
            field=wagtail.fields.StreamField(
                [("text", wagtail.blocks.RichTextBlock())], use_json_field=True
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="content",
            field=wagtail.fields.StreamField(
                [("text", wagtail.blocks.RichTextBlock())],
                blank=True,
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="standardpage",
            name="content",
            field=wagtail.fields.StreamField(
                [("text", wagtail.blocks.RichTextBlock())],
                blank=True,
                use_json_field=True,
            ),
        ),
    ]
