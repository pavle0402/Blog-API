from django.db import models
from django.contrib.auth.models import User
from . import validators

marriage_choices = (
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Divorced', 'Divorced'),
    ('In a relationship', 'In a relationship'),
    ()
)

class Hobbies(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f"{self.name}"


class ProfilePage(models.Model):
    class MarriageStatus(models.TextChoices):
        Single = 'Single', 'Single'
        Married = 'Married', 'Married'
        Divorced = 'Divorced', 'Divorced'
        In_a_relationship = 'In a relationship', 'In a relationship'

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='images', default='images/avatar.png')
    bio = models.TextField(blank=True)
    birthday = models.DateField(verbose_name="Birth date", validators=[validators.requires_age_of_18])
    workplace = models.CharField(max_length=255, blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, null=True)
    marriage_status = models.CharField(choices=MarriageStatus.choices, default=MarriageStatus.Single,
                                        max_length=len(MarriageStatus.In_a_relationship))
    hobbies = models.ManyToManyField(Hobbies)
    created_at = models.DateTimeField(auto_now_add=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    tiktok = models.URLField(blank=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.author.first_name} {self.author.last_name}'s profile"
    

    # def age_restrict(self):
