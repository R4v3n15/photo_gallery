# Generated by Django 2.0 on 2018-01-05 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180105_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='password',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
