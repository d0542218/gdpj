from django.contrib.auth.models import User
from rest_framework import serializers, request
from EsNoteScore.models import esNote_score_model, esNote_score_pic_model


class UserSerializer(serializers.HyperlinkedModelSerializer):
    esNote_score = serializers.HyperlinkedRelatedField(many=True, view_name='esnote_score_model-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'esNote_score')


class esNote_score_Serializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='user.username')
    esNote_score_pic = serializers.HyperlinkedRelatedField(many=True, view_name='esnote_score_pic_model-detail',
                                                           read_only=True)

    class Meta:
        model = esNote_score_model
        fields = ("noteID", "scoreName", "scoreStatus", "owner", "esNote_score_pic")


class change_score_name_Serializer(serializers.ModelSerializer):


    class Meta:
        model = esNote_score_model
        fields = ("scoreName",)

class esNote_score_pic_Serializer(serializers.HyperlinkedModelSerializer):
    belongTo = serializers.ReadOnlyField(source='esNote_score_pic_set')

    # esNote_score_pic = serializers.ListField(child=serializers.FileField(allow_empty_file=False))

    def create(self, validated_data):
        # print("VVVVVVVVVVVVVVVVVV")
        # print(validated_data)
        # esNote_score = validated_data.get('esNote_score')
        # print(esNote_score)
        image = validated_data.pop('esNote_score_pic')
        pic = esNote_score_pic_model.objects.create(esNote_score_pic=image, **validated_data)
        return pic

    class Meta:
        model = esNote_score_pic_model
        fields = ('esNote_score_noteID', 'esNote_score_pic','score_picModifyTime', 'belongTo','order')


class pic_Serializer(serializers.ModelSerializer):
    class Meta:
        model = esNote_score_pic_model
        fields = ('esNote_score_noteID','order', 'esNote_score_pic','esNote_score_resize_pic')


class searchPicSerializer(serializers.ModelSerializer):
    # esNote_score_pic = serializers.HyperlinkedRelatedField(many=True, view_name='esnote_score_pic_model-detail',
    #                                                        read_only=True)
    # esNote_score_pic = pic_Serializer(many=True, read_only=True)
    esNote_score_pic = serializers.SerializerMethodField()
    class Meta:
        model = esNote_score_model
        fields = ('noteID','esNote_score_pic')

    def get_esNote_score_pic(self, instance):
        score_pics = instance.esNote_score_pic.all().order_by('order')
        return pic_Serializer(score_pics, many=True).data


class historySerializer(serializers.ModelSerializer):
    # esNote_score_pic = pic_Serializer(many=True, read_only=True)
    esNote_score_pic = serializers.SerializerMethodField()

    class Meta:
        model = esNote_score_model
        fields = ("noteID", "scoreName", "scoreStatus","scoreCreateTime","scoreModifyTime", "esNote_score_pic",)
    def get_esNote_score_pic(self, instance):
        score_pics = instance.esNote_score_pic.all().order_by('order')
        return pic_Serializer(score_pics, many=True).data