# Generated by Django 2.2 on 2019-11-22 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EsNoteScore', '0014_auto_20191102_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='esnote_score_model',
            name='media',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
