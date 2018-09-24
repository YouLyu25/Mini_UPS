
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Person(models.Model):
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    
    def __str__(self):
        return self.username


class package(models.Model):
    trackingid = models.CharField(max_length=30)
    STATUS = (
        ('C', 'Created'),
        ('E', 'truck en route to warehouse'),
        ('W', 'truck waiting for package'),
        ('O', 'out for delivery'),)
    status = models.CharField(max_length=30, choices=STATUS)

    def __str__(self):
        return self.trackingid

class Event(models.Model):
    ROLES = (
        ('O', 'Owner'),
        ('V', 'Vender'),
        ('G', 'Guest'),)
    PLUSONE = (
        ('Y', 'Yes'),
        ('N', 'No'),)

    username = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    
    role = models.CharField(max_length=1, choices=ROLES)
    guest = ArrayField(models.CharField(max_length=50), null=True)
    vender = ArrayField(models.CharField(max_length=50), null=True)
    name = models.CharField(max_length=100)
    date = models.CharField(max_length=50)
    plusOne = models.CharField(max_length=1, choices=PLUSONE)
    textQuestion = models.CharField(max_length=500, default="null")
    
    def __str__(self):
        return self.name



class Question(models.Model):
    VENDERPERMISSION = (
        ('Y', 'Yes'),
        ('N', 'No'),)
    FINALIZED = (
        ('Y', 'Yes'),
        ('N', 'No'),)
    username = models.CharField(max_length=30)
    eventName = models.CharField(max_length=100)
    name = models.CharField(max_length=500)
    options = ArrayField(models.CharField(max_length=500, default="foo"))
    venderPermission = models.CharField(max_length=1, choices=VENDERPERMISSION)
    finalized = models.CharField(max_length=1, choices=FINALIZED)
    
    def __str__(self):
        return self.name



class Guest(models.Model):
    username = models.CharField(max_length=30)
    eventName = models.CharField(max_length=100)
    eventOwner = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.username



class Vender(models.Model):
    username = models.CharField(max_length=30)
    eventName = models.CharField(max_length=100)
    eventOwner = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.username



class Response(models.Model):
    username = models.CharField(max_length=30)
    eventName = models.CharField(max_length=100)
    textResponse = ArrayField(models.CharField(max_length=500, default="foo"), null=True)
    multiResponse = ArrayField(models.CharField(max_length=500, default="foo"), null=True)

    def __str__(self):
        return self.username
