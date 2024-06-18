# Generated by Django 5.0.1 on 2024-02-13 08:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0006_kenindia_department_kenindia_location_and_more'),
        ('toner', '0007_remove_toner_request_department_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.DeleteModel(
            name='Kenindia_Department',
        ),
        migrations.DeleteModel(
            name='Kenindia_Location',
        ),
        migrations.AddField(
            model_name='toner_request',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]