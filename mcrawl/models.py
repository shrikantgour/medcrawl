from django.db import models

# Create your models here.

class paged(models.Model):
    pgno   =models.CharField(max_length = 4)
    bgtitle = models.CharField(max_length=200)
    bgauthor = models.CharField(max_length = 30)
    bgread =  models.CharField(max_length=20)
    bgdt = models.CharField(max_length=12)
    bgfdt = models.CharField(max_length=22)
    bglink  =models.CharField(max_length=250)
    bgpage = models.CharField(max_length = 250,null=True)
    bgtag1 =models.CharField(max_length=20,null=True)
    bgtag2 =models.CharField(max_length=20,null=True)
    bgtag3 =models.CharField(max_length=20,null=True)
    bgtag4 =models.CharField(max_length=20,null=True)
    bgtag5 =models.CharField(max_length=20,null=True)


class pgparam(models.Model):
    tag = models.CharField(max_length=20)
    num = models.IntegerField()
    relatedtags = models.CharField(max_length=200,null=True)