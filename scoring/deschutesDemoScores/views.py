from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Team, Score, Workout
from .totaling import totals
from .importing import DDDataImport


def index(request):
    template = loader.get_template('scoring/index.html')
    #TODO: accept workout arguments
    DDDataImport.importDDData()
    listOfScores = totals.getSingleWorkoutTotal(6)

    context = {'scores' : listOfScores}
    return HttpResponse(template.render(context, request))