from django.db import models

# Create your models here.
class paged(models.Model):
    
    pgno   =models.CharField(max_length = 5)
    title = models.CharField(max_length=150)
    read =  models.CharField(max_length=20)
    dt =models.CharField(max_length=12)
    gdt = models.CharField(max_length=22)
    link  =models.CharField(max_length=150)
    tags =models.CharField(max_length=150)#models.IntegerField()
