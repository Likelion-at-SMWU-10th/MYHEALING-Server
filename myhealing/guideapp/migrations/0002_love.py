# Generated by Django 4.0.5 on 2022-08-13 23:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('guideapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Love',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('guide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='love', to='guideapp.guide')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='love', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
