from django.db import models
from django.contrib.auth.models import User
from GraduateProject import settings


class History(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    sheetMusicName = models.CharField(max_length=100)
    sheetMusicPicture = models.ImageField(upload_to='img')
    create_time = models.DateTimeField(auto_now_add=True)
