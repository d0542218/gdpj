# Generated by Django 2.2 on 2019-11-02 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EsNoteScore', '0013_esnote_simple_score_pic_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='esnote_simple_score_pic_model',
            name='simple_pic',
            field=models.ImageField(default='Images/noimg.png', null=True, upload_to=''),
        ),
    ]