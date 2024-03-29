from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
# from django.views.decorators.csrf import csrf_exempt 
# @csrf_exempt

# Create your views here.
# _*_coding:utf-8 _*_


def register(request):
    print(request);
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print("Errors", form.errors)
        if form.is_valid():
            form.save()
            return redirect('/index')
        else:
            return render(request, 'registration/registration.html', {'form': form})
    else:
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'registration/registration.html', context)


def LogoutView(request):
    print(request);
    logout(request)
    return redirect('/index')


def AccountView(request):
    print(request);
    if request.user.is_authenticated:
        return render(request, "profile.html")
    else:
        return redirect("index")