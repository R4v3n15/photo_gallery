# Generated by Django 2.0 on 2018-01-06 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20180105_1653'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='password',
        ),
    ]
