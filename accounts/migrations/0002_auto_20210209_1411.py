# Generated by Django 3.1.4 on 2021-02-09 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.district'),
        ),
        migrations.AddField(
            model_name='localsupervisor',
            name='town',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.town'),
        ),
    ]
