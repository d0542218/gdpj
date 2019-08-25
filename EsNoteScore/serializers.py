from django.contrib.auth.models import User
from rest_framework import serializers, request
from EsNoteScore.models import esNote_score_model, esNote_score_pic_model


class UserSerializer(serializers.HyperlinkedModelSerializer):
    esNote_score = serializers.HyperlinkedRelatedField(many=True, view_name='esnote_score_model-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username','esNote_score')



class esNote_score_Serializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='user.username')
    esNote_score_pic = serializers.HyperlinkedRelatedField(many=True, view_name='esnote_score_pic_model-detail', read_only=True)

    class Meta:
        model = esNote_score_model
        fields = ("noteID","scoreName", "scoreStatus", "scoreInfoJason","owner","esNote_score_pic")


class esNote_score_pic_Serializer(serializers.HyperlinkedModelSerializer):
    belongTo = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = esNote_score_pic_model
        fields = ('esNote_score_noteID','esNote_score_pic','score_picModifyTime','belongTo')
