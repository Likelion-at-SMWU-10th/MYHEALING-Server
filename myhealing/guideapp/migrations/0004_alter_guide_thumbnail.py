# Generated by Django 4.0.5 on 2022-07-26 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guideapp', '0003_guide_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guide',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='img/guide/'),
        ),
    ]
