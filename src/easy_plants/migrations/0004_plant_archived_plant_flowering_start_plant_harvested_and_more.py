# Generated by Django 5.1 on 2024-08-23 04:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easy_plants', '0003_alter_plantentry_options_alter_plantentry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='plant',
            name='flowering_start',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plant',
            name='harvested',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plant',
            name='start',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='plantentry',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
