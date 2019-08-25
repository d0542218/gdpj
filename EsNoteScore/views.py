from django.contrib.auth.models import User
from EsNoteScore.models import esNote_score_model, esNote_score_pic_model
from EsNoteScore.serializers import esNote_score_Serializer, esNote_score_pic_Serializer, UserSerializer
from rest_framework import viewsets, authentication, permissions
from . import permission


# Create your views here.

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    # permission_classes = (permission.IsOwnerOrAdmin,)
    serializer_class = UserSerializer



class EsNoteScoreViewSet(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permission.IsOwnerOrAdmin,)
    queryset = esNote_score_model.objects.all()
    serializer_class = esNote_score_Serializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EsNoteScorePicViewSet(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permission.IsOwnerOrAdmin,)
    queryset = esNote_score_pic_model.objects.all()
    serializer_class = esNote_score_pic_Serializer

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        print(self.request)
