# Generated by Django 3.1.4 on 2021-03-05 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_delete_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(2, 'governor'), (3, 'editor'), (4, 'district_officer'), (5, 'town_officer'), (6, 'supervisor_or_farmer')], null=True),
        ),
    ]
