from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.auth.models import User
from PIL import Image as Img, Image


# Create your models here.

class esNote_score_model(models.Model):
    noteID = models.AutoField(primary_key=True)
    scoreName = models.CharField(max_length=45)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='esNote_score', null=True)
    scoreCreateTime = models.DateTimeField(auto_now_add=True)
    scoreModifyTime = models.DateTimeField(auto_now=True)
    scoreStatus = models.IntegerField()
    media = models.FileField(null=True)


class esNote_score_pic_model(models.Model):
    esNote_score_noteID = models.AutoField(primary_key=True)
    order = models.IntegerField(null=None, default=0)
    esNote_score_pic = models.ImageField(max_length=100, null=False, default="Images/noimg.png")
    score_picModifyTime = models.DateTimeField(auto_now=True)
    esNote_score = models.ForeignKey(esNote_score_model, related_name='esNote_score_pic', on_delete=models.CASCADE)
    esNote_score_resize_pic = models.ImageField(max_length=100, null=False, default="Images/noimg.png")
    esNote_score_predict_pic = models.ImageField(max_length=100, null=False, default="Images/noimg.png")
    esNote_score_data = models.FileField(null=True)
    esNote_score_processed_data = models.FileField(null=True)


    def save(self, *args, **kwargs):
        if self.esNote_score_pic:
            img = Img.open(BytesIO(self.esNote_score_pic.read()))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            if hasattr(img, '_getexif'):
                orientation = 0x0112
                exif = img._getexif()
                if exif is not None and orientation in exif.keys():
                    orientation = exif[orientation]
                    rotations = {
                        3: Image.ROTATE_180,
                        6: Image.ROTATE_270,
                        8: Image.ROTATE_90
                    }
                    if orientation in rotations.keys():
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
            if width > 2000 and height > 2000:
                if width > height:
                    rate = 2000 / width
                else:
                    rate = 2000 / height
                resize.thumbnail((int(width * rate), int(height * rate)), Img.ANTIALIAS)
            resize.save(output2, format='JPEG', quality=70)
            output2.seek(0)
            self.esNote_score_resize_pic = InMemoryUploadedFile(output2, 'ImageField',
                                                                "samll_%s.jpg" % self.esNote_score_pic.name.split('.')[
                                                                    0],
                                                                'image/jpeg', output.__sizeof__, None)
        super(esNote_score_pic_model, self).save(*args, **kwargs)


class esNote_simple_score_pic_model(models.Model):
    simple_score_ID = models.AutoField(primary_key=True)
    simple_pic = models.ImageField(max_length=100, null=True, default="Images/noimg.png")
    score_pic = models.ForeignKey(esNote_score_pic_model, related_name='score_pic', on_delete=models.CASCADE)