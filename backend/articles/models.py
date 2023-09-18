from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return f"{self.name}"

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField()
    image = models.ImageField(upload_to='images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE, default=None, blank=True)

    def __str__(self):
        return f"{self.title} - {self.author.first_name} {self.author.last_name}"
    

    @property
    def posted_on(self):
        current_time = timezone.now()
        delta = current_time - self.created_at

        if delta.days > 0:
            if delta.days == 1:
                return f"{delta.days} day ago."
            else:
                return f"{delta.days} days ago."
            
        elif delta.seconds >= 3600:
            hours = delta.seconds // 3600
            if hours == 1:
                return f"{hours} hour ago."
            else:
                return f"{hours} hours ago."
        elif delta.seconds >= 60:
            minutes = delta.seconds // 60
            if minutes == 1:
                return f"{minutes} minute ago."
            else:
                return f"{minutes} minutes ago."
        
        else:
            seconds = delta.seconds
            if seconds < 30:
                return f"Just now."
            else:
                return f"{seconds} seconds ago."
            

#user profile
