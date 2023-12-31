# Generated by Django 4.0.2 on 2023-09-14 20:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hobbies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ProfilePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(default='images/avatar.png', upload_to='images')),
                ('bio', models.TextField(blank=True)),
                ('birthday', models.DateField(verbose_name='Birth date')),
                ('workplace', models.CharField(blank=True, max_length=255, null=True)),
                ('education', models.CharField(blank=True, max_length=255, null=True)),
                ('marriage_status', models.CharField(choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('In a relationship', 'In a relationship')], default='Single', max_length=17)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('instagram', models.URLField()),
                ('facebook', models.URLField()),
                ('linkedin', models.URLField()),
                ('github', models.URLField()),
                ('twitter', models.URLField()),
                ('tiktok', models.URLField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('hobbies', models.ManyToManyField(to='user_profile.Hobbies')),
            ],
        ),
    ]
