from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Person(models.Model):
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username

class Accounts(models.Model):
    ups_account = models.CharField(max_length=50)
    amazon_account = models.CharField(max_length=50)
    pos_x = models.CharField(max_length=30)
    pos_y = models.CharField(max_length=30)

    def __str__(self):
        return self.amazon_account

class time(models.Model):
    worldid = models.CharField(max_length=30,null=True,default="")
    trackingid = models.CharField(max_length=30)
    packageid = models.CharField(max_length=30,null=True,default="")
    c_time = models.CharField(max_length=100,null=True,default="")
    e_time = models.CharField(max_length=100,null=True,default="")
    w_time = models.CharField(max_length=100,null=True,default="")
    l_time = models.CharField(max_length=100,null=True,default="")
    o_time = models.CharField(max_length=100,null=True,default="")
    d_time = models.CharField(max_length=100,null=True,default="")

class item(models.Model):
    worldid = models.CharField(max_length=30,null=True,default="")
    trackingid = models.CharField(max_length=30)
    iteminfo = models.CharField(max_length=200)
    count = models.CharField(max_length=30,null=True,default="1")
    def __str__(self):
        return self.iteminfo

class package(models.Model):
    worldid = models.CharField(max_length=30,null=True,default="")
    username = models.CharField(max_length=30)
    trackingid = models.CharField(max_length=30)
    STATUS = (
        ('C', 'Created'),
        ('E', 'truck en route to warehouse'),
        ('W', 'truck waiting for package'),
        ('L', 'loaded and waiting for delivery'),
        ('O', 'out for delivery'),
        ('D', 'delivered'))
    status = models.CharField(max_length=30, choices=STATUS)
    position_x = models.CharField(max_length=30,null=True)
    position_y = models.CharField(max_length=30,null=True)
    packageid = models.CharField(max_length=30,null=True,default="")
    truckid = models.CharField(max_length=30,null=True,default="")
    def __str__(self):
        return self.trackingid

class truck(models.Model):
    worldid = models.CharField(max_length=30,null=True,default="")
    truckid = models.CharField(max_length=30)
    package_num = models.CharField(max_length=10,default="0")
    STATUS = (
        ('I', 'idel'),
        ('E', 'truck en route to warehouse'),
        ('W', 'truck waiting for package'),
        ('L', 'loaded and waiting for delivery'),
        ('O', 'out for delivery'))
    status = models.CharField(max_length=30, choices=STATUS)

class curr_world(models.Model):
    name = models.CharField(max_length=30,null=True,default="curr_world")
    worldid = models.CharField(max_length=30,null=True)

class tracking_number(models.Model):
    worldid = models.CharField(max_length=30,null=True)
    tracking_number = models.CharField(max_length=30,null=True)

