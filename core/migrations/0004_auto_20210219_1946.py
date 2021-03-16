# Generated by Django 3.1.4 on 2021-02-19 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210219_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crop',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='crop',
            name='harvest_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
    ]