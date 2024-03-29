# Generated by Django 3.2.7 on 2021-09-03 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_Client', models.CharField(max_length=30, verbose_name='Nama')),
                ('noTelp_Client', models.CharField(max_length=15, verbose_name='Phone')),
                ('email_Client', models.EmailField(max_length=254, verbose_name='Email')),
                ('alamat_Client', models.CharField(max_length=254, verbose_name='Alamat')),
                ('kecamatan_Client', models.CharField(blank=True, max_length=30, null=True, verbose_name='Kecamatan')),
                ('kelurahan_Client', models.CharField(blank=True, max_length=30, null=True, verbose_name='Kelurahan')),
                ('kodePos_Client', models.CharField(blank=True, max_length=30, null=True, verbose_name='Kode Pos')),
                ('kota_Client', models.CharField(max_length=30, verbose_name='Kota')),
                ('slug_Client', models.SlugField()),
            ],
            options={
                'verbose_name': 'Client',
            },
        ),
    ]
