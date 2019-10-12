from django.http import HttpResponse
from django.shortcuts import render, redirect
# from .models import History


def historyView(request):
    return render(request, "history.html")