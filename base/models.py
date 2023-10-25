from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    publishedDate = models.DateTimeField(auto_now_add=True)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Comments(models.Model):
    text = models.TextField()
    publishedDate = models.DateTimeField(auto_now_add=True)
    authorId = models.ForeignKey(User, on_delete=models.CASCADE)
    postId = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

class Likes(models.Model):
    idPost =  models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    isDeleted = models.BooleanField(default=False)

class UserDetails(models.Model):
    picture = models.ImageField(upload_to= 'profilepics', blank=True, null = True)
    banner = models.ImageField(upload_to= 'profilebanners', blank=True, null = True)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE, default= 0)

class UserBio(models.Model):
    bio = models.TextField()
    idUser = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    
class Phrase(models.Model):
    text = models.CharField(max_length=255)

class ChatBot(models.Model):
    location = models.CharField(max_length=14)
    response = models.CharField(max_length=14)
    text = models.TextField()