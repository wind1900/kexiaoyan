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

class Event(models.Model):
    title = models.CharField(max_length=40)
    content = models.TextField()
    date = models.DateField()
    attach = models.CharField(max_length=30)
    # event important level
    # level 1: very important
    level = models.IntegerField()
    def __unicode__(self):
        return u"{0} {1}".format(self.title, self.date)

class Memday(models.Model):
    # for the nth m day in a month, use n*100+m to represent
    name = models.CharField(max_length=20)
    month = models.IntegerField()
    day = models.IntegerField()
    lunar = models.BooleanField()
