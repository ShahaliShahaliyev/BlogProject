from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=20)
    subtitle = models.CharField(max_length=20)
    slug = models.SlugField()
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title


class IpModel(models.Model):
    ip = models.CharField(max_length=100)
    
    def __str__(self):
        return self.ip

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    views = models.ManyToManyField(IpModel,related_name="post_views",blank=True)

    def __str__(self):
        return self.title
    
    def total_views(self):
        return self.views.count()
    
class Info(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField()
    content = models.TextField()
    
    
    def __str__(self):
        return self.name

