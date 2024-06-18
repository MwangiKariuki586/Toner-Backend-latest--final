# Generated by Django 5.0.1 on 2024-02-12 04:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0004_alter_customuser_managers'),
        ('toner', '0003_alter_toner_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='toner.kenindia_department'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='toner.kenindia_location'),
        ),
    ]