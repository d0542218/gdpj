from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class esNote_score_model(models.Model):
    noteID = models.AutoField(primary_key=True)
    scoreName = models.CharField(max_length=45)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='esNote_score', null=True)
    scoreCreateTime = models.DateTimeField(auto_now_add=True)
    scoreModifyTime = models.DateTimeField(auto_now=True)
    scoreStatus = models.IntegerField()
    scoreInfoJason = models.FileField()


class esNote_score_pic_model(models.Model):
    esNote_score_noteID = models.AutoField(primary_key=True)
    esNote_score_pic = models.ImageField(max_length=100, null=False, default="Images/noimg.png")
    score_picModifyTime = models.DateTimeField(auto_now=True)
    esNote_score = models.ForeignKey(esNote_score_model, on_delete=models.CASCADE)
