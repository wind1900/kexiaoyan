from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=10)

class Material(models.Model):
    content = models.TextField()
    time = models.DateTimeField(auto_now = True)
    category = models.ForeignKey(Category)

class Event(models.Model):
    title = models.CharField(max_length=40)
    content = models.TextField()
    date = models.DateField()
    attach = models.CharField(max_length=30)

class Memday(models.Model):
    name = models.CharField(max_length=20)
    month = models.IntegerField()
    day = models.IntegerField()
    lunar = models.BooleanField()
