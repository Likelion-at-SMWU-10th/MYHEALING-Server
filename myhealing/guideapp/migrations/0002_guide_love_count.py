# Generated by Django 4.0.5 on 2022-08-15 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guideapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guide',
            name='love_count',
            field=models.IntegerField(default=0),
        ),
    ]
