from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
import  templates

# Create your views here.
# _*_coding:utf-8 _*_


def home(request):
    return render(request, "index.html")



