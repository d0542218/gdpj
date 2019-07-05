from rest_framework import serializers
from EsNoteScore.models import esNote_score_model, esNote_score_pic_model


class esNote_score_Serializer(serializers.ModelSerializer):
    class Meta:
        model = esNote_score_model
        fields = '__all__'
        # fields = ('id', 'song', 'singer', 'last_modify_date', 'created')


class esNote_score_pic_Serializer(serializers.ModelSerializer):
    class Meta:
        model = esNote_score_pic_model
        fields = '__all__'
