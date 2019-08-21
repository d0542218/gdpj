from djoser.conf import User
from rest_framework import serializers, request
from EsNoteScore.models import esNote_score_model, esNote_score_pic_model


class esNote_score_Serializer(serializers.ModelSerializer):
    current_user = serializers.SerializerMethodField('_user')

    # Use this method for the custom field
    def _user(self, obj):
        request = getattr(self.context, 'request', None)
        if request:
            return request.user

    class Meta:
        model = esNote_score_model
        # fields = '__all__'
        fields = ('current_user','scoreName', 'scoreStatus', 'scoreInfoJason')

    # def create(self,validated_data):
    #     esNote_score_model(
    #         user = validated_data['current_user'],
    #         scoreName=validated_data["scoreName"],
    #         scoreStatus=validated_data["scoreStatus"],
    #         scoreInfoJason=validated_data["scoreInfoJason"]
    #     )
    #     esNote_score_model.save()
    #     return esNote_score_model


class esNote_score_pic_Serializer(serializers.ModelSerializer):
    class Meta:
        model = esNote_score_pic_model
        fields = '__all__'

    # def create(self, validated_data):
    #     esNote_score_pic_model()
