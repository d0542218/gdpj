from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.historyView,name="history"),
    # path("",view.)
]