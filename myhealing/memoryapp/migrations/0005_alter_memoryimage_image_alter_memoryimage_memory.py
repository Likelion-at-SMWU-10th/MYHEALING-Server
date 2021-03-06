# Generated by Django 4.0.5 on 2022-07-26 16:26

from django.db import migrations, models
import django.db.models.deletion
import memoryapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('memoryapp', '0004_remove_memoryimage_thumbnail_memory_thumbnail_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memoryimage',
            name='image',
            field=models.ImageField(upload_to=memoryapp.models.MemoryImage.image_upload_path),
        ),
        migrations.AlterField(
            model_name='memoryimage',
            name='memory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='memoryapp.memory'),
        ),
    ]
