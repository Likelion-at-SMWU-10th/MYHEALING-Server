# Generated by Django 4.0.5 on 2022-08-16 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memoryapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memory',
            name='scope',
        ),
        migrations.AddField(
            model_name='memory',
            name='address',
            field=models.CharField(default='', max_length=50),
        ),
    ]
