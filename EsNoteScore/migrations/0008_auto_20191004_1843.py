# Generated by Django 2.2 on 2019-10-04 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EsNoteScore', '0007_esnote_score_pic_model_predict_score_pic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='esnote_score_pic_model',
            old_name='predict_score_pic',
            new_name='esNote_score_predict_pic',
        ),
    ]
