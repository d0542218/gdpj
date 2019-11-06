import base64
import json
from io import BytesIO
import requests
import rest_framework_simplejwt
from PIL import ImageDraw, ImageFont, Image as Img
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import QuerySet
from django.http import QueryDict, HttpResponse
from rest_framework.exceptions import ParseError, NotFound, AuthenticationFailed
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from EsNoteScore.models import esNote_score_model, esNote_score_pic_model, esNote_simple_score_pic_model
from EsNoteScore.serializers import esNote_score_Serializer, esNote_score_pic_Serializer, UserSerializer \
    , searchPicSerializer, historySerializer, change_score_name_Serializer
from rest_framework import viewsets, authentication, permissions, status, generics, mixins
from rest_framework_simplejwt.tokens import AccessToken
import rest_framework_simplejwt.exceptions
from urllib.parse import quote
import math
import zipfile


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
            except:
                raise AuthenticationFailed(detail='Authorization is Null.')
        else:
            serializer.save(user=self.request.user)


class EsNoteScorePicViewSet(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permission.IsOwnerOrAdmin,)
    queryset = esNote_score_pic_model.objects.all()
    serializer_class = esNote_score_pic_Serializer

    def create(self, request, *args, **kwargs):
        # print(request.data)
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
            except:
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
            # print("QDic")
            # print(QDic)
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


# permission staff wait
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


class model_get_predict_pictures(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = esNote_score_model.objects.all()
    notes = [{1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', -2: '*', -1: '8', 0: '`', 'dot': '.'},
             {1: 'q', 2: 'w', 3: 'e', 4: 'r', 5: 't', 6: 'y', 7: 'u', -2: 'I', -1: 'i', 0: 'p', 'dot': 'o'},
             {1: 'a', 2: 's', 3: 'd', 4: 'f', 5: 'g', 6: 'h', 7: 'j', -2: 'K', -1: 'k', 0: ';', 'dot': 'l'},
             {1: 'z', 2: 'x', 3: 'c', 4: 'v', 5: 'b', 6: 'n', 7: 'm', -2: '<', -1: ','},
             {1: '!', 2: '@', 3: '#', 4: '$', 5: '%', 6: '^', 7: '&', 'dot': '.'},
             {1: 'Q', 2: 'W', 3: 'E', 4: 'R', 5: 'T', 6: 'Y', 7: 'U', 'dot': 'o'},
             {1: 'A', 2: 'S', 3: 'D', 4: 'F', 5: 'G', 6: 'H', 7: 'J', 'dot': 'l'},
             {1: 'Z', 2: 'X', 3: 'C', 4: 'V', 5: 'B', 6: 'N', 7: 'M', },
             {'sharp': 'P', 'flat': ':', 'natural': 'L', 2: "O", }]

    def Pitch(self, temp, Clef):
        if (Clef == 'g'):
            if (temp < -4):
                pitch = '-1'
            elif (temp > 2):
                pitch = '1'
            elif (temp < 3 and temp > -5):
                pitch = '0'
            else:
                print("音高錯誤 " + str(temp))
        elif (Clef == 'f'):
            if (temp < -3):
                pitch = '-1'
            elif (temp > 3):
                pitch = '1'
            elif (temp < 4 and temp > -4):
                pitch = '0'
            else:
                print("音高錯誤 " + str(temp))
        elif (Clef == 'c'):
            if (temp < -0):
                pitch = '-1'
            elif (temp > 7):
                pitch = '1'
            elif (temp < 8 and temp > -1):
                pitch = '0'
            else:
                print("音高錯誤 " + str(temp))
        return pitch

    def Clef(self, temp, Clef):
        gClef = {0: 5, 1: 6, 2: 7, 3: 1, 4: 2, 5: 3, 6: 4}
        cClef = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7}
        fClef = {0: 4, 1: 5, 2: 6, 3: 7, 4: 1, 5: 2, 6: 3}
        if (Clef == 'g'):
            name = gClef[temp]
        elif (Clef == 'c'):
            name = cClef[temp]
        elif (Clef == 'f'):
            name = fClef[temp]
        return name

    def initClef(self, unit):
        if (unit['type'] == 'tonality'):
            if unit['Clef'] == 'G':
                so = int(unit['number'])
            elif unit['Clef'] == 'C':
                do = int(unit['number'])
            elif unit['Clef'] == 'F':
                fa = int(unit['number'])

    def createLines(self, lines):

        #     lineCount = 1
        #     sectionCount = 1

        so = None
        fa = None
        do = None

        Line = []
        returnLines = []
        returnUnit = {}
        returnSection = []

        tupleUnit = []
        group = []
        singleNames = []
        singlePitchs = []
        #     if(lines[0][0]['notes'][0]['type']=='tonality'):
        #         print(lines[0][0]['notes'][0]['type'])
        # #         if lines[0][0]['notes'][0]['Clef'] == 'G':
        # #             so = int(lines[0][0]['noyes'][0]['number'])
        # #         elif lines[0][0]['notes'][0]['Clef'] == 'C' :
        # #             do = int(lines[0][0]['noyes'][0]['number'])
        # #         elif lines[0][0]['notes'][0]['Clef'] == 'F' :
        # #             fa = int(lines[0][0]['noyes'][0]['number'])
        #     else:
        so = 8
        for line in lines:
            for section in line:
                notes = section['notes']
                for unit in notes:
                    #                 if((sectionCount == 1)and(lineCount == 1)and(unit['type'] != 'tonality')):
                    #                     so = 8;
                    #                 elif((sectionCount == 1)and(lineCount == 1)and(unit['type'] == 'tonality')):
                    #                     if unit['Clef'] == 'G':
                    #                         so = int(unit['number'])
                    #                     elif unit['Clef'] == 'C' :
                    #                         do = int(unit['number'])
                    #                     elif unit['Clef'] == 'F' :
                    #                         fa = int(unit['number'])
                    if (unit['type'] == 'note'):
                        for number in unit['number']:
                            number = int(number)
                            if (so != None):
                                singleNames.append(self.Clef(((number - so) % 7), 'g'))
                                singlePitchs.append(self.Pitch(number - so, 'g'))
                            elif (fa != None):
                                singleNames.append(self.Clef(((number - fa) % 7), 'f'))
                                singlePitchs.append(self.Pitch(number - so, 'f'))
                            elif (do != None):
                                singleNames.append(self.Clef(((number - so) % 7), 'c'))
                                singlePitchs.append(self.Pitch(number - so, 'c'))
                        returnUnit['bounding box'] = unit['bounding box']
                        returnUnit['type'] = 'single note'
                        returnUnit['name'] = singleNames
                        returnUnit['pitch'] = singlePitchs
                        returnUnit['length'] = unit['length']
                        returnUnit['dotted'] = unit['dotted']
                        returnUnit['accidental'] = unit['accidental']
                        returnSection.append(returnUnit)
                        returnUnit = {}
                        singleNames = []
                        singlePitchs = []
                    elif (unit['type'] == 'tuplet note'):
                        for number in unit['number']:
                            number = int(number)
                            if (so != None):
                                singleNames.append(self.Clef(((number - so) % 7), 'g'))
                                singlePitchs.append(self.Pitch(number - so, 'g'))
                            elif (fa != None):
                                singleNames.append(self.Clef(((number - fa) % 7), 'f'))
                                singlePitchs.append(self.Pitch(number - so, 'f'))
                            elif (do != None):
                                singleNames.append(self.Clef(((number - so) % 7), 'c'))
                                singlePitchs.append(self.Pitch(number - so, 'c'))
                        returnUnit['name'] = singleNames
                        returnUnit['pitch'] = singlePitchs
                        returnUnit['length'] = unit['length']
                        returnUnit['bounding box'] = unit['bounding box']
                        returnUnit['dotted'] = unit['dotted']
                        returnUnit['accidental'] = unit['accidental']
                        group.append(returnUnit)
                        singleNames = []
                        returnUnit = {}
                        singlePitchs = []
                    elif (unit['type'] == 'tuplet end'):
                        for number in unit['number']:
                            number = int(number)
                            if (so != None):
                                singleNames.append(self.Clef(((number - so) % 7), 'g'))
                                singlePitchs.append(self.Pitch(number - so, 'g'))
                            elif (fa != None):
                                singleNames.append(self.Clef(((number - fa) % 7), 'f'))
                                singlePitchs.append(self.Pitch(number - so, 'f'))
                            elif (do != None):
                                singleNames.append(self.Clef(((number - so) % 7), 'c'))
                                singlePitchs.append(self.Pitch(number - so, 'c'))
                        returnUnit['name'] = singleNames
                        returnUnit['pitch'] = singlePitchs
                        returnUnit['length'] = unit['length']
                        returnUnit['bounding box'] = unit['bounding box']
                        returnUnit['dotted'] = unit['dotted']
                        returnUnit['accidental'] = unit['accidental']
                        group.append(returnUnit)
                        returnSection.append({'type': 'tuple note', 'group': group})
                        singleNames = []
                        group = []
                        returnUnit = {}
                        singlePitchs = []
                    elif (unit['type'] == 'rest'):
                        returnUnit['type'] = 'rest'
                        returnUnit['length'] = unit['length']
                        returnUnit['dotted'] = unit['dotted']
                        returnUnit['bounding box'] = unit['bounding box']
                        returnSection.append(returnUnit)
                        returnUnit = {}
                #             sectionCount+=1
                Line.append(returnSection)
                returnSection = []
            #         lineCount+=1
            #         sectionCount=0
            returnLines.append(Line)
            Line = []
        return returnLines

    def first_collection(self, inputjson):
        with open('inputjson.json', 'w') as outfile:
            json.dump(inputjson, outfile)
        returnJson = {}
        returnJson['duet'] = inputjson['duet']
        firstLines = []
        secondLines = []
        if (inputjson['duet'] == True):
            for i in len(inputjson['lines']):
                if (i % 2 == 0):
                    firstLines.append(inputjson['lines'][i])
                else:
                    secondLines.append(inputjson['lines'][i])
            returnJson['lines'] = self.createLines(firstLines) + self.createLines(secondLines)
        else:
            returnJson['lines'] = self.createLines(inputjson['lines'])
        with open('returnJson.json', 'w') as outfile:
            json.dump(returnJson, outfile)
        return self.create_all_bar(returnJson)

    def use_pitch_get_char(self, name, pitch, length, space, dotted, multiple=False, end=False):

        returnstr = ''
        org = -1
        if length == 0 or length == 2:
            org = length
            length = 4
        if multiple or end:
            returnstr += '起'
        if pitch == 0:
            returnstr += self.notes[int(math.log(length, 2)) - 2][name]
        elif pitch == 1:
            returnstr += self.notes[int(math.log(length, 2)) - 2 + 4][name]
        elif pitch == 2:
            returnstr += self.notes[int(math.log(length, 2)) - 2][name]
            if length != 4:
                returnstr += self.notes[8][pitch]
            else:
                returnstr += '~'
        else:  # -2,-1
            returnstr += self.notes[int(math.log(length, 2)) - 2][name]
            returnstr += self.notes[int(math.log(length, 2)) - 2][pitch]
        if dotted == 1:
            returnstr += self.notes[int(math.log(length, 2)) - 2]['dot']
        if org == 0:
            returnstr += "///"
        if org == 2:
            returnstr += "/"
        if space:
            returnstr += ' '
        if end:
            returnstr += '末'
        return returnstr

    def single_note_return(self, names, pitch, length, dotted, accidental, space=True):
        # name is a list heigh count need a soulution
        # need to add space
        returnstr = ''
        if accidental != "none":
            returnstr += self.notes[8][accidental]
        if len(names) == 1:
            returnstr += self.use_pitch_get_char(names[0], int(pitch[0]), int(length), space, dotted)
        if len(names) != 1:
            returnstr += self.use_pitch_get_char(names[0], int(pitch[0]), int(length), space, dotted, multiple=True)
            returnstr += self.use_pitch_get_char(names[1], int(pitch[1]), int(length), space, dotted, end=True)
        return returnstr

    def rest_return(self, length, dotted):
        returnstr = ''
        length = int(length)

        if length == 0:
            returnstr += '````'
        if length == 2:
            returnstr += '``'
        else:
            returnstr += self.notes[int(math.log(int(length) - 2, 2))][0]
        if dotted == 1:
            returnstr += self.notes[int(math.log(length, 2)) - 2]['dot']
        returnstr += ' '
        return returnstr

    def tuple_note_return(self, group):
        # no need to ad space
        returnstr = ''
        for i in group:
            # print(i['name'], i['pitch'], i['length'], i['dotted'], i['accidental'])
            returnstr += self.single_note_return(i['name'], i['pitch'], i['length'], i['dotted'], i['accidental'],
                                                 space=False)
        returnstr += ' '
        return returnstr

    def draw(self, img, site, texts, font=ImageFont.truetype(settings.BASE_DIR + '/01SMN.ttf', 22)):
        draw = ImageDraw.Draw(img)
        draw.text(tuple(site), texts, (0, 0, 0), font=font)

    def createimg(self):
        a4 = (595, 842)
        img = Img.new('RGB', a4, (245, 245, 220))
        return img

    def create_all_bar(self, jf):
        lineCount = jf['duet']
        lines = jf["lines"]
        all_bar = []

        for line in lines:
            for bars in line:
                all_bar.append('\\')
                for Note in bars:
                    if Note['type'] == "single note":
                        # print((Note['name'], Note['pitch'], Note['length'], Note['dotted'], Note['accidental']))
                        all_bar.append(
                            self.single_note_return(Note['name'], Note['pitch'], Note['length'], Note['dotted'],
                                                    Note['accidental']))
                    if Note['type'] == 'rest':
                        # print('rest\n' + Note['length'])
                        all_bar.append(self.rest_return(Note['length'], Note['dotted']))
                    if Note['type'] == 'tuple note':
                        # print('group')
                        all_bar.append(self.tuple_note_return(Note['group']))
        #             print(all_bar[-1])
        all_bar.append('\\')
        return self.draw_simple_score(all_bar)

    def draw_simple_score(self, all_bar):
        font = ImageFont.truetype(settings.BASE_DIR + '/01SMN.ttf', 22)
        limit = (595 - 30, 842 - 30)
        site = [15, 30]
        line = ''
        imglist = []
        gap = 15
        page = 1
        # print(all_bar)
        dualList = []
        length_of_all_bar = len(all_bar)

        for i, bar in enumerate(all_bar):
            change = False
            daul = "起" in bar
            if daul:
                words = bar.split('起')
                #         print(word)
                temp = ''
                for j, word in enumerate(words):
                    #             print(word)
                    if j == 0:
                        pass
                    elif (j % 2 == 1):
                        pri = temp
                        temp += word
                    else:
                        #                 print('temp   '+temp)
                        dualx, dualword = font.getsize(line + pri)[0], word.split('末')[0]
                        #                 print((line+pri,dualword))
                        dualList.append((dualx, dualword))
                #         all_bar[i]= bar.split('起')[1]
                bar = temp
            linewid, linehig = font.getsize(line + bar)
            barwid, barhig = font.getsize(bar)
            if (linewid <= limit[0]):  # 沒換行
                line += bar
            else:
                change = True
            if length_of_all_bar - 1 == i:
                # print('fffffinal')
                change = True
            if change:
                if not imglist:
                    img = self.createimg()
                    imglist.append(img)
                if limit[0] - linewid + barwid >= 75:
                    line += " \\"
                self.draw(imglist[-1], site, line)
                if dualList:
                    for i in range(len(dualList)):
                        a = dualList.pop()
                        #                 print('draw ',a)
                        #                 print(site)
                        #                 print(a[0]+site[0],site[1])
                        self.draw(imglist[-1], (a[0] + site[0], site[1] - 25), a[1])
                if (int(site[1]) + gap + int(linehig) <= int(limit[1])):  # 換行且沒換頁
                    # print(bar + '換行沒換頁')
                    site = [15, int(site[1]) + gap + int(linehig)]
                    line = bar
                else:  # 換行且換頁
                    # print(bar + '換行換頁')
                    page += 1
                    img = self.createimg()
                    imglist.append(img)
                    site = [15, 30]
        # for i in imglist:
        # i.show()
        return imglist

    def list(self, request, *args, **kwargs):
        res = []
        url = "http://140.134.26.63:15001/predict_by_url"
        # url = "http://127.0.0.1:5000/predict_by_url"
        ip = "http://140.134.26.63:18000/media/"
        ip2 = "http://182.155.209.64:18000/media/"
        if self.request.user == AnonymousUser():
            try:
                token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
                access_token = AccessToken(token)
                user = User.objects.get(id=int(access_token['user_id']))
            except rest_framework_simplejwt.exceptions.TokenError:
                raise AuthenticationFailed(detail='Token is invalid or expired.')
            except:
                raise AuthenticationFailed(detail='Authorization is Null.')
        else:
            user = self.request.user
        if not request.GET.get('id'):
            raise ParseError("id is null")
        if not request.GET.get('order'):
            raise ParseError("order is null")
        # if not request.GET.get('reask'):
        #     reask =False
        esNote_score__noteID = request.GET.get('id')
        order = request.GET.get('order')
        try:
            pic_model = esNote_score_pic_model.objects.filter(esNote_score__noteID=esNote_score__noteID, order=order)[0]
            owner = esNote_score_model.objects.filter(noteID=esNote_score__noteID)[0].user
        except IndexError:
            raise NotFound("please check id and order.")
        if not (user == owner or request.user.is_staff):
            raise AuthenticationFailed("Permission deny.")
        return_json = {}
        if not (pic_model.esNote_score_data):
            try:
                # print(ip2 + quote(str(pic_model.esNote_score_resize_pic)))
                r = requests.request("POST", url, data={"img_url": ip2 + quote(str(pic_model.esNote_score_resize_pic))})
                print(r.status_code)
                if r.status_code != 200:
                    raise ParseError("remote server error", code=r.status_code)
                score = r.json()
                file = ContentFile(json.dumps(score))
                pic_model.esNote_score_data.save("predict_data_%s.json" % pic_model.esNote_score_pic.name.split('.')[0],
                                                 file)
            except requests.exceptions.ConnectionError:
                raise ParseError("remote server closed.", code=500)
        else:
            with pic_model.esNote_score_data.open() as file:
                score = json.load(file)
        try:
            with open('score.json', 'w') as outfile:
                json.dump(score, outfile)
            input = {}
            input['lines'] = score
            input['duet'] = False
            im = Img.open(BytesIO(pic_model.esNote_score_resize_pic.read()))
            for line in score:
                for bar in line:
                    for note in bar["notes"]:
                        bbox = note["bounding box"]
                        ystart = bbox[1] - bbox[3] / 2
                        yend = bbox[1] + bbox[3] / 2
                        xstart = bbox[0] - bbox[2] / 2
                        xend = bbox[0] + bbox[2] / 2
                        draw = ImageDraw.Draw(im)
                        draw.line([(xstart, ystart), (xend, ystart)], fill="blue", width=2)
                        draw.line([(xstart, ystart), (xstart, yend)], fill="blue", width=2)
                        draw.line([(xend, ystart), (xend, yend)], fill="blue", width=2)
                        draw.line([(xstart, yend), (xend, yend)], fill="blue", width=2)
            output_buffer = BytesIO()
            im.save(output_buffer, format='JPEG')
            # im.show()
            output_buffer.seek(0)
            # pic_model.esNote_score_predict_pic.save("predit_%s.jpg" % pic_model.esNote_score_pic.name.split('.')[0],
            #                                         output_buffer, save=True)
            # print(pic_model.esNote_score_pic.url)
            byte_data = output_buffer.getvalue()
            base64_str = base64.b64encode(byte_data)
            im.close()
            imglist = self.first_collection(input)
            for i in esNote_simple_score_pic_model.objects.filter(score_pic=pic_model):
                i.delete()
            for index, i in enumerate(imglist):
                i.save(output_buffer, format='JPEG')
                p = esNote_simple_score_pic_model(score_pic=pic_model)
                p.save()
                p.simple_pic.save("simple_%s_%s.jpg" % (pic_model.esNote_score_pic.name.split('.')[0], str(index)),
                                  output_buffer, save=True)
            simple_url = []
            for i in esNote_simple_score_pic_model.objects.filter(score_pic=pic_model):
                simple_url.append(i.simple_pic.url)
                return_json['simple_url'] = simple_url
        except Exception as e:
            print(e)

        return_json["pic"] = base64_str
        output_buffer.close()
        return Response(return_json)


class model_get_history(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = esNote_score_model.objects.all()
    page = True
    serializer_class = historySerializer

    def get_queryset(self):
        if self.request.user == AnonymousUser():
            try:
                token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
                access_token = AccessToken(token)
                user = User.objects.get(id=int(access_token['user_id']))
            except rest_framework_simplejwt.exceptions.TokenError:
                raise AuthenticationFailed(detail='Token is invalid or expired.')
            except:
                raise AuthenticationFailed(detail='Authorization is Null.')
        else:
            user = self.request.user
        return esNote_score_model.objects.filter(user=user)


class model_get_fake_predict_pictures(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = esNote_score_model.objects.all()

    def list(self, request, *args, **kwargs):
        return_json = {}
        if self.request.user == AnonymousUser():
            try:
                token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
                access_token = AccessToken(token)
                user = User.objects.get(id=int(access_token['user_id']))
            except rest_framework_simplejwt.exceptions.TokenError:
                raise AuthenticationFailed(detail='Token is invalid or expired.')
            except:
                raise AuthenticationFailed(detail='Authorization is Null.')
        else:
            user = self.request.user
        if not request.GET.get('id'):
            raise ParseError("id is null")
        if not request.GET.get('order'):
            raise ParseError("order is null")
        esNote_score__noteID = request.GET.get('id')
        order = request.GET.get('order')
        try:
            pic_model = esNote_score_pic_model.objects.filter(esNote_score__noteID=esNote_score__noteID, order=order)[0]
            esNote_score = esNote_score_model.objects.filter(noteID=esNote_score__noteID)[0]
            owner = esNote_score_model.objects.filter(noteID=esNote_score__noteID)[0].user
        except IndexError:
            raise NotFound("please check id and order.")
        if not (user == owner or request.user.is_staff):
            raise AuthenticationFailed("Permission deny.")
        if not (pic_model.esNote_score_data):
            print("no file.")
            a = {"this is a json": True}
            myfile = ContentFile(json.dumps(a))
            pic_model.esNote_score_data.save("test.json", myfile)
        else:
            with pic_model.esNote_score_data.open() as file:
                data = json.load(file)
                print(data)

        img = Img.open(BytesIO(pic_model.esNote_score_resize_pic.read()))
        output_buffer = BytesIO()
        img.save(output_buffer, format='JPEG')
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data)

        imglist = []
        imglist.append(output_buffer)
        imglist.append(output_buffer)
        for i in esNote_simple_score_pic_model.objects.filter(score_pic=pic_model):
            i.delete()
        for im in imglist:
            p = esNote_simple_score_pic_model(score_pic=pic_model)
            p.save()
            p.simple_pic.save("simple_%s.jpg" % pic_model.esNote_score_pic.name.split('.')[0],
                              im, save=True)
        img.close()
        simple_url = []
        for i in esNote_simple_score_pic_model.objects.filter(score_pic=pic_model):
            simple_url.append(i.simple_pic.url)

        return_json['simple_url'] = simple_url
        return_json["pic"] = base64_str
        output_buffer.close()
        return Response(return_json)


class change_score_name(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    queryset = esNote_score_model.objects.all()
    serializer_class = change_score_name_Serializer

    def update(self, request, *args, **kwargs):
        print(request.data)
        if self.request.user == AnonymousUser():
            try:
                token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
                access_token = AccessToken(token)
                user = User.objects.get(id=int(access_token['user_id']))
            except rest_framework_simplejwt.exceptions.TokenError:
                raise AuthenticationFailed(detail='Token is invalid or expired.')
            except:
                raise AuthenticationFailed(detail='Authorization is Null.')
        else:
            user = self.request.user
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # print(instance)
        # print(instance.user)
        if not (user == instance.user or request.user.is_staff):
            raise AuthenticationFailed("Permission deny.")
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class change_order_of_pics(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    queryset = esNote_score_model.objects.all()

    def update(self, request, *args, **kwargs):
        new_order = request.data.get('new_order').split(',')
        instance = self.get_object()
        pic_model = esNote_score_pic_model.objects.filter(esNote_score=instance).order_by('order')
        # print(pic_model)
        if len(new_order) != len(new_order):
            raise ParseError("please check length of list.")
        copy = new_order[:]
        copy.sort()
        for index, order in enumerate(copy):
            order = int(order)
            if index + 1 != order:
                raise ParseError("please check order of list.")
        for i, j in zip(pic_model, new_order):
            i.order = int(j)
            i.save()
        return Response("ok")


class get_simple_score(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = esNote_score_model.objects.all()

    def list(self, request, *args, **kwargs):
        PDF = False
        ZIP = False
        if self.request.user == AnonymousUser():
            try:
                token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
                access_token = AccessToken(token)
                user = User.objects.get(id=int(access_token['user_id']))
            except rest_framework_simplejwt.exceptions.TokenError:
                raise AuthenticationFailed(detail='Token is invalid or expired.')
            except:
                raise AuthenticationFailed(detail='Authorization is Null.')
        else:
            user = self.request.user
        if not request.GET.get('id'):
            raise ParseError("id is null")
        if request.GET.get('fileType'):
            if request.GET.get('fileType') == 'PDF':
                PDF = True
            elif request.GET.get('fileType') == 'ZIP':
                ZIP = True
            else:
                raise ParseError("no support this fileType.")
        else:
            raise ParseError("please fill fileType.")
        if PDF and ZIP:
            raise ParseError("please only fill in PDF or ZIP")
        esNote_score__noteID = request.GET.get('id')
        try:
            pic_model = esNote_score_pic_model.objects.filter(esNote_score__noteID=esNote_score__noteID, order=1)[0]
            esNote_score = esNote_score_model.objects.filter(noteID=esNote_score__noteID)[0]
            owner = esNote_score_model.objects.filter(noteID=esNote_score__noteID)[0].user
        except IndexError:
            raise NotFound("please check id.")
        if not (user == owner or request.user.is_staff):
            raise AuthenticationFailed("Permission deny.")
        scoreName = esNote_score.scoreName
        simple_score_pics = esNote_simple_score_pic_model.objects.filter(score_pic=pic_model)
        imglist = []

        for simple_score in simple_score_pics:
            im = Img.open(BytesIO(simple_score.simple_pic.read()))
            imglist.append(im)
        if scoreName != 'deafault':
            font = ImageFont.truetype('PingFangTC.ttf', 22)
            draw = ImageDraw.Draw(imglist[0])
            draw.text(((imglist[0].size[0] - font.getsize(scoreName)[0]) / 2, 10), scoreName, (0, 0, 0), font=font)
        return_json = {}
        if ZIP:
            zip_file = BytesIO()
            with zipfile.ZipFile(zip_file, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
                for index, img in enumerate(imglist):
                    output_buffer = BytesIO()
                    img.save(output_buffer, format='JPEG')
                    zf.writestr('%s_%d.jpg' % (scoreName, index), output_buffer.getvalue())
            base64_str = base64.b64encode(zip_file.getvalue())
            return_json['filename'] = '%s.zip' % (scoreName)
            return_json["file"] = base64_str
            zip_file.close()
            output_buffer.close()
            return Response(return_json)
        elif PDF:
            pdf_file = BytesIO()
            output_buffer = BytesIO()
            imglist[0].save(pdf_file, "PDF", resolution=100.0, save_all=True, append_images=imglist[1:])
            base64_str = base64.b64encode(pdf_file.getvalue())
            return_json['filename'] = "%s.pdf" % (scoreName)
            return_json["file"] = base64_str
            pdf_file.close()
            output_buffer.close()
            return Response(return_json)
