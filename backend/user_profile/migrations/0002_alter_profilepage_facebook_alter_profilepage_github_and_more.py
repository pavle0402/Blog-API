# Generated by Django 4.0.2 on 2023-09-15 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepage',
            name='facebook',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='profilepage',
            name='github',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='profilepage',
            name='instagram',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='profilepage',
            name='linkedin',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='profilepage',
            name='tiktok',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='profilepage',
            name='twitter',
            field=models.URLField(blank=True),
        ),
    ]