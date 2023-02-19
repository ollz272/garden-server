# Generated by Django 4.1.5 on 2023-01-29 13:37

import wagtail.admin.forms.choosers
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("navigation", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="headerlinks",
            name="header_links",
            field=wagtail.fields.StreamField(
                [
                    (
                        "link",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "link",
                                    wagtail.blocks.StructBlock(
                                        [
                                            (
                                                "link_to",
                                                wagtail.blocks.ChoiceBlock(
                                                    choices=[
                                                        ("page", "Page"),
                                                        ("file", "File"),
                                                        ("custom_url", "Custom URL"),
                                                        ("email", "Email"),
                                                        ("anchor", "Anchor"),
                                                        ("phone", "Phone"),
                                                    ],
                                                    classname="link_choice_type_selector",
                                                    label="Link to",
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "page",
                                                wagtail.blocks.PageChooserBlock(
                                                    form_classname="page_link",
                                                    label="Page",
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "file",
                                                wagtail.documents.blocks.DocumentChooserBlock(
                                                    form_classname="file_link",
                                                    label="File",
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "custom_url",
                                                wagtail.blocks.CharBlock(
                                                    form_classname="custom_url_link url_field",
                                                    label="Custom URL",
                                                    max_length=300,
                                                    required=False,
                                                    validators=[
                                                        wagtail.admin.forms.choosers.URLOrAbsolutePathValidator()
                                                    ],
                                                ),
                                            ),
                                            (
                                                "anchor",
                                                wagtail.blocks.CharBlock(
                                                    form_classname="anchor_link",
                                                    label="#",
                                                    max_length=300,
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "email",
                                                wagtail.blocks.EmailBlock(
                                                    required=False
                                                ),
                                            ),
                                            (
                                                "phone",
                                                wagtail.blocks.CharBlock(
                                                    form_classname="phone_link",
                                                    label="Phone",
                                                    max_length=30,
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "new_window",
                                                wagtail.blocks.BooleanBlock(
                                                    form_classname="new_window_toggle",
                                                    label="Open in new window",
                                                    required=False,
                                                ),
                                            ),
                                        ],
                                        label=False,
                                    ),
                                ),
                                (
                                    "link_text",
                                    wagtail.blocks.CharBlock(label="Link text"),
                                ),
                            ],
                            label="link",
                            required=False,
                        ),
                    )
                ],
                blank=True,
                help_text="Shown to all users. A maximum of 5 can be added",
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="headerlinks",
            name="logged_in_header_links",
            field=wagtail.fields.StreamField(
                [
                    (
                        "link",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "link",
                                    wagtail.blocks.StructBlock(
                                        [
                                            (
                                                "link_to",
                                                wagtail.blocks.ChoiceBlock(
                                                    choices=[
                                                        ("page", "Page"),
                                                        ("file", "File"),
                                                        ("custom_url", "Custom URL"),
                                                        ("email", "Email"),
                                                        ("anchor", "Anchor"),
                                                        ("phone", "Phone"),
                                                    ],
                                                    classname="link_choice_type_selector",
                                                    label="Link to",
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "page",
                                                wagtail.blocks.PageChooserBlock(
                                                    form_classname="page_link",
                                                    label="Page",
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "file",
                                                wagtail.documents.blocks.DocumentChooserBlock(
                                                    form_classname="file_link",
                                                    label="File",
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "custom_url",
                                                wagtail.blocks.CharBlock(
                                                    form_classname="custom_url_link url_field",
                                                    label="Custom URL",
                                                    max_length=300,
                                                    required=False,
                                                    validators=[
                                                        wagtail.admin.forms.choosers.URLOrAbsolutePathValidator()
                                                    ],
                                                ),
                                            ),
                                            (
                                                "anchor",
                                                wagtail.blocks.CharBlock(
                                                    form_classname="anchor_link",
                                                    label="#",
                                                    max_length=300,
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "email",
                                                wagtail.blocks.EmailBlock(
                                                    required=False
                                                ),
                                            ),
                                            (
                                                "phone",
                                                wagtail.blocks.CharBlock(
                                                    form_classname="phone_link",
                                                    label="Phone",
                                                    max_length=30,
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "new_window",
                                                wagtail.blocks.BooleanBlock(
                                                    form_classname="new_window_toggle",
                                                    label="Open in new window",
                                                    required=False,
                                                ),
                                            ),
                                        ],
                                        label=False,
                                    ),
                                ),
                                (
                                    "link_text",
                                    wagtail.blocks.CharBlock(label="Link text"),
                                ),
                            ],
                            label="link",
                            required=False,
                        ),
                    )
                ],
                blank=True,
                help_text="Only shown to logged in users. Standard header links will be shown if this list is empty. A maximum of 5 can be added.",
                use_json_field=True,
            ),
        ),
    ]
