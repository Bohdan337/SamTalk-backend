# Generated by Django 5.1.1 on 2025-03-10 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_customuser_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile_images/image.jpg', null=True, upload_to='profile_images/'),
        ),
    ]
