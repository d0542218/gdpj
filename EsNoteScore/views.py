import json
import os
from io import BytesIO

import requests
import rest_framework_simplejwt
from PIL import ImageDraw, Image
from django.contrib.auth.models import User, AnonymousUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import QuerySet
from django.http import QueryDict
from rest_framework.exceptions import ParseError, NotFound, AuthenticationFailed
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from EsNoteScore.models import esNote_score_model, esNote_score_pic_model
from EsNoteScore.serializers import esNote_score_Serializer, esNote_score_pic_Serializer, UserSerializer \
    , searchPicSerializer
from rest_framework import viewsets, authentication, permissions, status, generics, mixins
from rest_framework_simplejwt.tokens import AccessToken
import rest_framework_simplejwt.exceptions

from GraduateProject import settings
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
        if self.request.user == AnonymousUser():
            try:
                print(self.request.META)
                token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
                access_token = AccessToken(token)
                user = User.objects.get(id=int(access_token['user_id']))
                serializer.save(user=user)
            except rest_framework_simplejwt.exceptions.TokenError:
                raise AuthenticationFailed(detail='Token is invalid or expired.')
            except :
                raise AuthenticationFailed(detail='Authorization is Null.')
        else:
            serializer.save(user=self.request.user)



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
    order = 0

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
        if self.request.user == AnonymousUser():
            try:
                print(self.request.META)
                token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
                access_token = AccessToken(token)
                user = User.objects.get(id=int(access_token['user_id']))
                serializer.save(user=user)
            except rest_framework_simplejwt.exceptions.TokenError:
                raise AuthenticationFailed(detail='Token is invalid or expired.')
            except :
                raise AuthenticationFailed(detail='Authorization is Null.')
        else:
            serializer.save(user=self.request.user)
        self.noteID = int(dict(serializer.data).get('noteID'))
        self.return_data.update(serializer.data)
        # print(serializer.data)
        # print(self.noteID)

    def create(self, request, *args, **kwargs):
        # print(request.data)
        self.order = 0
        self.temp.clear()
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
        if not pic.getlist('esNote_score_pic'):
            raise ParseError(detail="esNote_score_pic is Null.")
        for i in pic.getlist('esNote_score_pic'):
            self.order += 1
            QDic.update({'esNote_score_pic': i})
            print("QDic")
            print(QDic)
            serializer = self.get_serializer(data=QDic)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        self.querysetflag = 0
        self.serializerflag = 0
        self.return_data.update({'esNote_score_pic': self.temp})

        return Response(self.return_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(esNote_score=esNote_score_model.objects.get(noteID=self.noteID), order=self.order)
        self.temp.append(serializer.data)


class model_get_pictures(viewsets.GenericViewSet, mixins.ListModelMixin):
    model = esNote_score_model
    serializer_class = searchPicSerializer
    queryset = esNote_score_model.objects.all()
    id = None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        if self.id is None:
            raise ParseError(detail="Has no id.")
        serializer = self.get_serializer(queryset, many=True)
        if not serializer.data:
            raise NotFound(detail="id error or no data.")
        return Response(serializer.data)

    def get_queryset(self):
        self.id = self.request.GET.get('id')
        return esNote_score_model.objects.filter(noteID=self.id)

#
#
#
#
# class model_get_predict_pictures(viewsets.GenericViewSet, mixins.ListModelMixin):
#     model = esNote_score_model
#     serializer_class = predictPicSerializer
#     secserializer_class = searchPicSerializer
#     queryset = esNote_score_model.objects.all()
#     noteID=0
#     modlist=[]
#
#     def list(self, request, *args, **kwargs):
#         res=[]
#         queryset = esNote_score_model.objects.filter(noteID=request.GET.get('id'))
#         self.modlist = esNote_score_pic_model.objects.filter(esNote_score__noteID=request.GET.get('id'))
#         secserializer = self.secserializer_class(queryset, many=True)
#         j = json.loads(JSONRenderer().render(secserializer.data))
#         print(j)
#         self.noteID = j[0].get("noteID")
#         piclist = j[0].get("esNote_score_pic")
#         j=0
#         for i in piclist:
#             print(i.get('esNote_score_resize_pic'))
#             res.append(draw(j,i.get('esNote_score_resize_pic'),self.modlist))
#             j+=1
#         return Response(res)
#
#
# def draw(site, filepath,modlist):
#     r = requests.post('http://127.0.0.1:5000/', json={"img_url": "http://127.0.0.1:8000/" + filepath})
#     im = Image.open(settings.BASE_DIR+'/'+settings.MEDIA_URL+filepath.split('/')[-1])
#     bar_array = r.json()
#     output = BytesIO()
#     for bar in bar_array:
#         for note in bar["notes"]:
#             bbox = note["bounding box"]
#             ystart = bbox[1] - bbox[3] / 2
#             yend = bbox[1] + bbox[3] / 2
#             xstart = bbox[0] - bbox[2] / 2
#             xend = bbox[0] + bbox[2] / 2
#             rectangleWithwidth([xstart, xend, ystart, yend], "blue", im, width=5,)
#     output.seek(0)
#     im.save(output, format='JPEG', quality=70)
#     img = InMemoryUploadedFile(output, 'ImageField', "predict_%s.jpg" % filepath.split("/")[-1],
#                                'image/jpeg', output.__sizeof__, None)
#     modlist[site].update(predict_score_pic=img)
#     return "http://127.0.0.1:8000/" +"predict_%s.jpg" % filepath.spilt("/")[-1]
#         # self.serializer.save(esNote_score=esNote_score_model.objects.get(noteID=self.noteID), order=self.order)
#
#
# def rectangleWithwidth(list, color, file, width=5):
#     draw = ImageDraw.Draw(file)
#     # list[0] = xs,list[1] = xend ,list[2] = ys,list[3] = yend,
#     assert len(list) == 4
#     assert list is not None
#     draw.line([(list[0], list[2]), (list[1], list[2])], fill=color, width=width)
#     draw.line([(list[0], list[2]), (list[0], list[3])], fill=color, width=width)
#     draw.line([(list[1], list[2]), (list[1], list[3])], fill=color, width=width)
#     draw.line([(list[0], list[3]), (list[1], list[3])], fill=color, width=width)