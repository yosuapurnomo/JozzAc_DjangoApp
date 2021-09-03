# Generated by Django 3.2.7 on 2021-09-03 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SPKModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_SPK', models.CharField(blank=True, max_length=30, unique=True, verbose_name='Nomor SPK')),
                ('tgl_input', models.DateField(auto_now=True, verbose_name='Tanggal Input')),
                ('tgl_pengerjaan', models.DateField(verbose_name='Tanggal Pengerjaan')),
                ('keterangan', models.TextField(verbose_name='Keterangan')),
                ('status', models.CharField(choices=[('PENDING', 'ON PROGRESS'), ('CANCEL', 'CANCEL'), ('SELESAI', 'SELESAI')], default='PENDING', max_length=10)),
                ('slug_SPK', models.SlugField()),
            ],
            options={
                'verbose_name': 'Surat Perintah Kerja',
                'verbose_name_plural': 'Surat Perintah Kerja',
            },
        ),
    ]