# Generated by Django 2.2 on 2019-09-28 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EsNoteScore', '0005_esnote_score_pic_model_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='esnote_score_pic_model',
            name='esNote_score_resize_pic',
            field=models.ImageField(default='Images/noimg.png', upload_to=''),
        ),
    ]
