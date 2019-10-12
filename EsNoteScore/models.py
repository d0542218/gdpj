import time
from io import BytesIO

import requests
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.auth.models import User
from PIL import Image as Img, ImageDraw, Image


# Create your models here.


class esNote_score_model(models.Model):
    noteID = models.AutoField(primary_key=True)
    scoreName = models.CharField(max_length=45)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='esNote_score', null=True)
    scoreCreateTime = models.DateTimeField(auto_now_add=True)
    scoreModifyTime = models.DateTimeField(auto_now=True)
    scoreStatus = models.IntegerField()
    scoreInfoJason = models.FileField(null=True)


class esNote_score_pic_model(models.Model):
    esNote_score_noteID = models.AutoField(primary_key=True)
    order = models.IntegerField(null=None, default=0)
    esNote_score_pic = models.ImageField(max_length=100, null=False, default="Images/noimg.png")
    score_picModifyTime = models.DateTimeField(auto_now=True)
    esNote_score = models.ForeignKey(esNote_score_model, related_name='esNote_score_pic', on_delete=models.CASCADE)
    esNote_score_resize_pic = models.ImageField(max_length=100, null=False, default="Images/noimg.png")
    esNote_score_predict_pic = models.ImageField(max_length=100, null=False, default="Images/noimg.png")

    def save(self, *args, **kwargs):
        if self.esNote_score_pic:
            img = Img.open(BytesIO(self.esNote_score_pic.read()))
            print(self.esNote_score_pic.name)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            if hasattr(img, '_getexif'):
                orientation = 0x0112
                exif = img._getexif()
                if exif is not None and orientation in exif.keys():
                    print("yes")
                    orientation = exif[orientation]
                    rotations = {
                        3: Image.ROTATE_180,
                        6: Image.ROTATE_270,
                        8: Image.ROTATE_90
                    }
                    if orientation in rotations.keys():
                        print(orientation)
                        img = img.transpose(rotations[orientation])
            resize = img.copy()
            output = BytesIO()
            img.save(output, format='JPEG', quality=70)
            output.seek(0)
            self.esNote_score_pic = InMemoryUploadedFile(output, 'ImageField',
                                                         "%s.jpg" % hash(self.esNote_score_pic.name.split('.')[0]),
                                                         'image/jpeg', output.__sizeof__, None)
            # wait for detail
            output2 = BytesIO()
            width, height = resize.size
            if width > 1000 and height > 1000:
                if width > height:
                    rate = 1000 / width
                else:
                    rate = 1000 / height
                resize.thumbnail((int(width * rate), int(height * rate)), Img.ANTIALIAS)
            resize.save(output2, format='JPEG', quality=70)
            output2.seek(0)
            self.esNote_score_resize_pic = InMemoryUploadedFile(output2, 'ImageField',
                                                                "samll_%s.jpg" % self.esNote_score_pic.name.split('.')[
                                                                    0],
                                                                'image/jpeg', output.__sizeof__, None)
        super(esNote_score_pic_model, self).save(*args, **kwargs)
