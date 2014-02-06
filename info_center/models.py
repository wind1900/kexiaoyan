# -*- coding:utf-8 -*-

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=10)
    def __unicode__(self):
        return self.name

class Material(models.Model):
    content = models.TextField()
    time = models.DateTimeField(auto_now = True)
    category = models.ForeignKey(Category)
    def __unicode__(self):
        return u"#{0}# {1}".format(self.category, self.content)
    class Meta:
        ordering = ('-time',)

class Event(models.Model):
    title = models.CharField(max_length=40)
    date = models.DateField()
    attach = models.CharField(max_length=30, blank=True)
    # event important level
    # level 1: very important
    level = models.IntegerField(default=2)
    def __unicode__(self):
        return u"{0} {1}".format(self.title, self.date)
    class Meta:
        ordering = ('-date',)

class FetionText(models.Model):
    content = models.TextField()
    date = models.DateField()
    def __unicode__(self):
        return str(self.date)
    class Meta:
        ordering = ('-date',)

class Memday(models.Model):
    # for the nth m day in a month, use n*100+m to represent
    # Monday == 1 ... Sunday == 7
    name = models.CharField(max_length=20)
    month = models.IntegerField()
    day = models.IntegerField()
    lunar = models.BooleanField()
    def __unicode__(self):
        return self.name

class Birthday(models.Model):
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)
    month = models.IntegerField()
    day = models.IntegerField()
    lunar = models.BooleanField()
    def __unicode__(self):
        return u"{0}({1})的生日".format(self.name, self.phone)
