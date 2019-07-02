# from django.db import models
#
# # Create your models here.
# class esNote_score_model(models.Model):
#     noteID = models.AutoField(primary_key=True)
#     scoreName = models.CharField(max_length=45)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='esNote_score')
#     scoreCreateTime = models.DateTimeField(auto_now_add=True)
#     scoreModifyTime = models.DateTimeField(auto_now=True)
#     scoreStatus = models.IntegerField()
#     scoreInfoJason = models.CharField(max_length=100)
