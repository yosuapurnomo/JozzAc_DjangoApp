# Generated by Django 3.1.1 on 2021-07-17 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210705_1926'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': 'Account', 'verbose_name_plural': 'Account'},
        ),
        migrations.AlterField(
            model_name='account',
            name='is_admin',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]