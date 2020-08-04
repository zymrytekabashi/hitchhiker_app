
from django.db import models
import re
from datetime import datetime, date
import bcrypt
from django.core.validators import MaxValueValidator, MinValueValidator



class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):                
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] ='Password should be at least 8 characters'
        if postData['password'] != postData['conf_password']:
            errors['conf_password'] = 'Passwords should match'         
        result = User.objects.filter(email=postData['email'])
        if len(result) > 0:
            errors['email'] = 'Email has already been registered!'
            
        return errors
    

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        
        if len(postData['location']) < 2:
            errors["location"] = "Location should be at least 2 characters"
        if len(postData['desc']) < 10:
            errors["desc"] = "Description should be at least 10 characters"            
        return errors 
    
class Trip(models.Model):
    location = models.CharField(max_length=255)
    seats = models.IntegerField(default=1, validators=[MaxValueValidator(7), MinValueValidator(1)])
    desc = models.TextField()
    posted_by = models.ForeignKey(User, related_name='has_trips', on_delete=models.CASCADE)
    reserve_seat = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
    
    
class CommentManager(models.Manager):
    def comment_validator(self, postData):
        errors = {}
        
        if len(postData['comment']) < 5:
            errors["comment"] = "Comment should be at least 5 characters"        
        return errors 
    
    
class Comment(models.Model):
    comment=models.CharField(max_length=255)
    poster=models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    trip= models.ForeignKey(Trip, related_name='comments', on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="liked_comments")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = CommentManager()