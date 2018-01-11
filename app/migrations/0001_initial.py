# Generated by Django 2.0 on 2017-12-22 18:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=870)),
                ('thumb', models.ImageField(upload_to='albums_thumb')),
                ('tags', models.CharField(max_length=250)),
                ('is_visible', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AlbumImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='albums')),
                ('thumb', models.ImageField(upload_to='albums/thumbs')),
                ('alt', models.CharField(default=uuid.uuid4, max_length=255)),
                ('width', models.IntegerField(default=900)),
                ('height', models.IntegerField(default=506)),
                ('slug', models.CharField(default=uuid.uuid4, editable=False, max_length=70)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Album')),
            ],
        ),
    ]