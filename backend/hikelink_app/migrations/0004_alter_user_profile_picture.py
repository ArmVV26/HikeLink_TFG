# Generated by Django 5.2.1 on 2025-05-15 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hikelink_app', '0003_alter_routerating_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
