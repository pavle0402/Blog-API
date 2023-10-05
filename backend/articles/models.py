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
            

class CommentSection(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', default=None)
    

    def __str__(self):
        if not self.parent_comment:
            return f"Comment by {self.author} on post {self.article.title}"
        else:
            return f"Reply by {self.author} on {self.parent_comment.author}'s comment."


    @property
    def is_parent(self):
        if self.parent_comment is not None:
            return False
        return True
    
    def children(self):
        return CommentSection.objects.filter(parent_comment=self)

    @property
    def created_at(self):
        current_time = timezone.now()
        delta = current_time - self.posted_on

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
            