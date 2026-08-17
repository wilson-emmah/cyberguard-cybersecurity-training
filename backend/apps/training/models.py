from django.contrib.auth.models import User
from django.db import models
class Course(models.Model):
 title=models.CharField(max_length=200); slug=models.SlugField(unique=True); description=models.TextField(); category=models.CharField(max_length=100); published=models.BooleanField(default=True); order=models.PositiveIntegerField(default=0)
 def __str__(self): return self.title
class Scenario(models.Model):
 title=models.CharField(max_length=200); scenario_type=models.CharField(max_length=20,choices=[('phishing','Phishing'),('url','Suspicious URL'),('password','Password Security'),('malware','Malware')]); description=models.TextField(); prompt=models.TextField(); choices=models.JSONField(default=list); correct_choice=models.PositiveIntegerField(); explanation=models.TextField(); points=models.PositiveIntegerField(default=100); published=models.BooleanField(default=True); course=models.ForeignKey(Course,null=True,blank=True,on_delete=models.SET_NULL)
 def __str__(self): return self.title
class Attempt(models.Model):
 user=models.ForeignKey(User,on_delete=models.CASCADE); scenario=models.ForeignKey(Scenario,on_delete=models.CASCADE); selected_choice=models.PositiveIntegerField(); correct=models.BooleanField(); points_awarded=models.PositiveIntegerField(default=0); created_at=models.DateTimeField(auto_now_add=True)
