# Generated by Django 4.0.5 on 2022-08-11 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='', max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(default='', max_length=15, unique=True),
        ),
    ]
