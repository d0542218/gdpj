# Generated by Django 2.2 on 2019-10-04 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EsNoteScore', '0006_esnote_score_pic_model_esnote_score_resize_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='esnote_score_pic_model',
            name='predict_score_pic',
            field=models.ImageField(default='Images/noimg.png', upload_to=''),
        ),
    ]