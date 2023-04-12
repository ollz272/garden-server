# Generated by Django 4.0.6 on 2022-07-24 19:55

from django.conf import settings
from django.db import migrations


def make_tokens(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Token = apps.get_model("authtoken", "Token")
    for user in User.objects.all():
        Token.objects.get_or_create(user=user)


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("authtoken", "0003_tokenproxy"),
    ]

    operations = [migrations.RunPython(make_tokens)]