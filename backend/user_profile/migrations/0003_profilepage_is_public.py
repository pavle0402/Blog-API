# Generated by Django 4.0.2 on 2023-09-16 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_alter_profilepage_facebook_alter_profilepage_github_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilepage',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
    ]
