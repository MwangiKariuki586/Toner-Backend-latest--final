# Generated by Django 5.0.1 on 2024-02-13 07:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toner', '0006_toner_request__previous_issued'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='toner_request',
            name='Department',
        ),
        migrations.RemoveField(
            model_name='toner_request',
            name='Location',
        ),
        migrations.RemoveField(
            model_name='toner_request',
            name='Staff_ID',
        ),
        migrations.RemoveField(
            model_name='toner_request',
            name='Staff_name',
        ),
        migrations.RemoveField(
            model_name='toner_request',
            name='_previous_issued',
        ),
        migrations.AlterField(
            model_name='toner_request',
            name='printer_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='toner.printer'),
        ),
    ]
