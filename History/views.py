from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import History


def historyView(request):
    if request.method == "POST":
        userID = None
        if request.user.is_authenticated:
            userID = request.user
        name = request.POST.get("sheetMusicName")
        print(name)
        pic = request.FILES.get('sheetMusicPicture')
        history = History(author=userID, sheetMusicName=name, sheetMusicPicture=pic)
        history.save()
        return redirect("/history")
    else:
        if request.user.is_authenticated:
            historydb = History.objects.filter(author=request.user)
            context = {'history': historydb}
            return render(request, "history.html", context)
        else:
            return redirect('/index')
