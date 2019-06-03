from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Team, Score


def index(request):
    listOfScores = Score.objects.all()
    template = loader.get_template('scoring/index.html')
    context = {'scores' : listOfScores}
    return HttpResponse(template.render(context, request))