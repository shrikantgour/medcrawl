from django.db import models

# Create your models here.

class paged(models.Model):
    pgno   =models.CharField(max_length = 4)
    bgtitle = models.CharField(max_length=200,null=True)
    bgauthor = models.CharField(max_length = 30,null=True)
    bgread =  models.CharField(max_length=20,null=True)
    bgdt = models.CharField(max_length=12,null=True)
    bgfdt = models.CharField(max_length=22,null=True)
    bglink  =models.CharField(max_length=250)
    bgpage = models.CharField(max_length = 250,null=True)
    bgtag1 =models.CharField(max_length=20,null=True)
    bgtag2 =models.CharField(max_length=20,null=True)
    bgtag3 =models.CharField(max_length=20,null=True)
    bgtag4 =models.CharField(max_length=20,null=True)
    bgtag5 =models.CharField(max_length=20,null=True)


class pgparam(models.Model):
    tag = models.CharField(max_length=20)
    prevtag = models.CharField(max_length=20)
    num = models.IntegerField()
    startnum = models.IntegerField(null=True)
    endnum = models.IntegerField(null=True)
    remainingarticles = models.IntegerField(null=True)
    subfromtoday =  models.IntegerField(null=True)
    relatedtags = models.CharField(max_length=200,null=True)
    errcode = models.IntegerField(null=True)
    scrapetime = models.FloatField(null = True)
    loopcount=models.IntegerField(null=True)