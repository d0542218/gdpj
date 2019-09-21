from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import QueryDict
from rest_framework.response import Response
from EsNoteScore.models import esNote_score_model, esNote_score_pic_model
from EsNoteScore.serializers import esNote_score_Serializer, esNote_score_pic_Serializer, UserSerializer
from rest_framework import viewsets, authentication, permissions, status
from rest_framework_simplejwt.tokens import AccessToken
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

    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #     data = request.data
    #     print(data)
    #     serializer = self.get_serializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(data)
    #     print(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #     # return Response('serializer', status=status.HTTP_201_CREATED)
    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(type(serializer.data))
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
            # print("hihi")
        except:
            token = self.request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            access_token = AccessToken(token)
            user = User.objects.get(id=int(access_token['user_id']))
            serializer.save(user=user)
        pass


class EsNoteScorePicViewSet(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permission.IsOwnerOrAdmin,)
    queryset = esNote_score_pic_model.objects.all()
    serializer_class = esNote_score_pic_Serializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return Response('serializer', status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

class upload_images(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permission.IsOwnerOrAdmin,)
    queryset = esNote_score_model.objects.all()
    serializer_class = esNote_score_Serializer
    sec_queryset = esNote_score_pic_model.objects.all()
    sec_serializer_class = esNote_score_pic_Serializer
    serializerflag = 0
    querysetflag = 0
    noteID = None
    return_data = {}
    temp = []

    def get_queryset(self):
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )
        queryset = self.queryset
        if self.serializerflag == 1:
            queryset = self.sec_queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def get_serializer_class(self):
        if self.serializerflag == 1:
            return self.sec_serializer_class
        else:
            return self.serializer_class

    def build_default_Esnote(self):
        defaultScore = {'scoreName': 'deafault', 'scoreStatus': 0}
        QDdefaultScore = QueryDict('', mutable=True)
        QDdefaultScore.update(defaultScore)
        serializer = self.get_serializer(data=QDdefaultScore)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(user=self.request.user)
            # print("hihi")
        except:
            token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            access_token = AccessToken(token)
            user = User.objects.get(id=int(access_token['user_id']))
            serializer.save(user=user)
        self.noteID = int(dict(serializer.data).get('noteID'))
        self.return_data.update(serializer.data)
        # print(serializer.data)
        print(self.noteID)

    def create(self, request, *args, **kwargs):
        self.build_default_Esnote()
        QDic = QueryDict('', mutable=True)
        self.querysetflag = 1
        self.serializerflag = 1
        pic = request.FILES
        # print(pic.getlist('esNote_score_pic'))
        # print(request.data)
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        for i in pic.getlist('esNote_score_pic'):
            QDic.update({'esNote_score_pic': i})
            # print(QDic)
            serializer = self.get_serializer(data=QDic)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        self.querysetflag = 0
        self.serializerflag = 0
        self.return_data.update({'esNote_score_pic':self.temp})
        return Response(self.return_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(esNote_score=esNote_score_model.objects.get(noteID=self.noteID))
        self.temp.append(serializer.data)
