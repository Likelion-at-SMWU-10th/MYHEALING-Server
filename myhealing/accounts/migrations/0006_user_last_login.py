# Generated by Django 4.0.5 on 2022-08-14 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_user_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
