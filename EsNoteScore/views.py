from django.shortcuts import render

# Create your views here.
from EsNoteScore.models import esNote_score_model, esNote_score_pic_model
from EsNoteScore.serializers import esNote_score_Serializer, esNote_score_pic_Serializer
from rest_framework import viewsets, authentication, permissions


# Create your views here.

class EsNoteScoreView(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = esNote_score_model.objects.all()
    serializer_class = esNote_score_Serializer


class EsNoteScorePicView(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = esNote_score_pic_model.objects.all()
    serializer_class = esNote_score_pic_Serializer
