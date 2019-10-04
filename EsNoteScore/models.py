from io import BytesIO

import requests
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.auth.models import User
from PIL import Image as Img, ImageDraw


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
    order = models.IntegerField(null=None,default=0)
    esNote_score_pic = models.ImageField(max_length=100, null=False, default="Images/noimg.png")
    score_picModifyTime = models.DateTimeField(auto_now=True)
    esNote_score = models.ForeignKey(esNote_score_model,related_name='esNote_score_pic', on_delete=models.CASCADE)
    esNote_score_resize_pic = models.ImageField(max_length=100, null=False, default="Images/noimg.png")
    esNote_score_predict_pic = models.ImageField(max_length=100, null=False, default="Images/noimg.png")

    def save(self, *args, **kwargs):
        if self.esNote_score_pic:
            img = Img.open(BytesIO(self.esNote_score_pic.read()))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            resize = img.copy()
            output = BytesIO()
            img.save(output, format='JPEG', quality=70)
            output.seek(0)
            self.esNote_score_pic = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.esNote_score_pic.name.split('.')[0],
                                              'image/jpeg', output.__sizeof__, None)
            # wait for detail
            output2 = BytesIO()
            width, height = resize.size
            if width>height:
                rate = 1000 / width
            else:
                rate = 1000 / height
            resize.thumbnail((int(width*rate), int(height*rate)), Img.ANTIALIAS)
            resize.save(output2, format='JPEG', quality=70)
            output2.seek(0)
            self.esNote_score_resize_pic= InMemoryUploadedFile(output2, 'ImageField', "samll_%s.jpg" % self.esNote_score_pic.name.split('.')[0],
                                              'image/jpeg', output.__sizeof__, None)
        # super(esNote_score_pic_model, self).save(*args, **kwargs)
        if self.esNote_score_resize_pic:
            print("http://127.0.0.1:8000/media/" + self.esNote_score_resize_pic.name)
            r = requests.post('http://127.0.0.1:5000/', json={"img_url": "http://127.0.0.1:8000/media/" + self.esNote_score_resize_pic.name})
            im = Img.open(BytesIO(self.esNote_score_resize_pic.read()))
            bar_array = r.json()
            for bar in bar_array:
                for note in bar["notes"]:
                    bbox = note["bounding box"]
                    ystart = bbox[1] - bbox[3] / 2
                    yend = bbox[1] + bbox[3] / 2
                    xstart = bbox[0] - bbox[2] / 2
                    xend = bbox[0] + bbox[2] / 2
                    draw = ImageDraw.Draw(im)
                    draw.line([(xstart, ystart), (xend, ystart)], fill="blue", width=5)
                    draw.line([(xstart, ystart), (xstart,yend)], fill="blue", width=5)
                    draw.line([(xend, ystart), (xend, yend)], fill="blue", width=5)
                    draw.line([(xstart, yend), (xend, yend)], fill="blue", width=5)
                    # self.rectangleWithwidth([xstart, xend, ystart, yend], "blue", im, width=5)
            output3 = BytesIO()
            im.save(output3, format='JPEG', quality=70)
            im.save('D:/PycharmProject/pillowTest/out222.jpg', 'JPEG')
            output3.seek(0)
            self.esNote_score_predict_pic = InMemoryUploadedFile(output3, 'ImageField', "predict %s.jpg" % self.esNote_score_pic.name.split('.')[0],
                                              'image/jpeg', output3.__sizeof__, None)
        super(esNote_score_pic_model, self).save(*args, **kwargs)