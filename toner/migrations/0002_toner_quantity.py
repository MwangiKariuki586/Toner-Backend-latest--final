# Generated by Django 5.0.1 on 2024-02-01 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='toner',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]