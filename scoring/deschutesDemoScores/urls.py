from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('finalResults', views.finalResults, name='finalResults'),
    path('scoreInput', views.scoreInput, name='scoreInput'),
    path('scoreInputReceived', views.scoreInputReceived, name='scoreInputReceived'),
    path('accounts/login/', auth_views.LoginView.as_view()),

]