# Generated by Django 5.1 on 2024-12-19 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easy_plants', '0008_plant_yield_dry_plant_yield_wet'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='yield_kief',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
