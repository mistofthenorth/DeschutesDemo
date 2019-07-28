from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Team, Score
from .totaling import totals


def index(request):
    template = loader.get_template('scoring/index.html')
    #TODO: accept workout arguments
    listOfScores = totals.getSingleWorkoutTotal(6)
    context = {'scores' : listOfScores}
    return HttpResponse(template.render(context, request))