# Generated by Django 3.1.4 on 2021-02-19 08:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locations', '0004_town_officer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='officer',
            field=models.ManyToManyField(blank=True, limit_choices_to={'roles__id': 4}, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='town',
            name='officer',
            field=models.ManyToManyField(blank=True, limit_choices_to={'roles__id': 5}, to=settings.AUTH_USER_MODEL),
        ),
    ]
