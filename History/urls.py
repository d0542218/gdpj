from django.urls import path, include
from . import views

urlpatterns = [
    path('history', views.historyView, name="history"),
]
