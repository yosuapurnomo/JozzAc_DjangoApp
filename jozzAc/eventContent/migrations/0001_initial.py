# Generated by Django 3.2.7 on 2021-09-03 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import eventContent.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='eventContentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_Content', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to=eventContent.models.upload_location)),
                ('keterangan_Content', models.TextField()),
                ('tgl_upload', models.DateField(auto_now_add=True)),
                ('slug_Content', models.SlugField()),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event',
            },
        ),
    ]
