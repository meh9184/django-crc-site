from django.db import models
from django.core.validators import URLValidator


class Entries(models.Model):                                                          
    aid = models.BigIntegerField()
    title = models.CharField(max_length=60)                                           
    content = models.TextField()                                                      
    aDate = models.DateTimeField()
    nUrl = models.TextField(validators=[URLValidator()])
    pUrl = models.TextField(validators=[URLValidator()])
    subClass = models.CharField(max_length=10)
    nClass = models.CharField(max_length=10)
    press = models.CharField(max_length=10, default=None, null=True)
    pdf = models.CharField(max_length=20, default=None, null=True)
    numComment = models.IntegerField(default=0)

    def __unicode__(self):
        return self.pUrl


class Comments(models.Model):
    cid = models.ForeignKey(Entries, on_delete=models.CASCADE,)
    cDate = models.CharField(max_length=20)
    comment = models.TextField()
    nClass = models.CharField(max_length=10)

    def __unicode__(self):
        return self.cid


class CheckContent(models.Model):
    ccid = models.AutoField(primary_key=True)
    checkField = models.IntegerField()
    user = models.CharField(max_length=50)
    contentId = models.IntegerField()

    def __unicode__(self):
        return self.user


class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    aid = models.CharField(max_length=10, default=None,null=True)
    atitle = models.CharField(max_length=60, default=None,null=True)
    asentence = models.TextField(default=None, null=True)
    asubject = models.CharField(max_length=40,default=None,null=True)
    aobejct = models.CharField(max_length=40,default=None,null=True)
    averb = models.CharField(max_length=40,default=None,null=True)
    acomplement = models.CharField(max_length=40,default=None,null=True)
    aetc = models.CharField(max_length=40,default=None,null=True)
    subjectflag = models.CharField(max_length=10,default=None,null=True)
    objectflag = models.CharField(max_length=10,default=None,null=True)
    verbflag = models.CharField(max_length=10,default=None,null=True)
    etcflag = models.CharField(max_length=10,default=None,null=True)
    passiveflag = models.CharField(max_length=10,default=None,null=True)
    articleDate = models.CharField(max_length=20)
    apress = models.CharField(max_length=10)
    uid = models.CharField(max_length=60, default=None, null=True)

    def __unicode__(self):
        return self.aid


class Url(models.Model):
    noUrl = models.AutoField(primary_key=True)
    noParent = models.IntegerField()
    value = models.CharField(max_length=200, default=None,null=True)
    depth = models.IntegerField()

    def __unicode__(self):
        return self.value