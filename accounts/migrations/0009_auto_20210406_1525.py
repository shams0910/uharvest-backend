# Generated by Django 3.1.4 on 2021-04-06 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210406_1520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='username',
        ),
        migrations.AddField(
            model_name='account',
            name='passport_number',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]