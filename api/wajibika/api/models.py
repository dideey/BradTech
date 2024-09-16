from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class County(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Constituency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    county = models.ForeignKey(County, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Ward(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Leaders(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image = models.URLField()
    county = models.ForeignKey(County, null=True, blank=True, on_delete=models.CASCADE)
    constituency = models.ForeignKey(Constituency, null=True, blank=True, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, null=True, blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    leader = models.ForeignKey(Leaders, on_delete=models.CASCADE)

class Video(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True, null=True)

class Image(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True, null=True)

class Text(models.Model):
    text = models.TextField()

class PostContent(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content', 'object_id')

class PostComment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    image = models.URLField(max_length=1000, blank=True, null=True)
