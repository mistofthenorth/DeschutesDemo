from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Team, Score, Workout
from .totaling import totals
from .importing import DDDataImport


def index(request):
    try:
        print(request.POST['workout'])
        workout = request.POST['workout']
    except:
        print('no post available')
        workout = 6
    print('workout number is ' + str(workout))
    template = loader.get_template('scoring/index.html')
    #TODO: accept workout arguments
    #DDDataImport.importDDTeams()
    #DDDataImport.importDDData()
    listOfWorkouts = Workout.objects.filter(event = 1)
    #print(listOfWorkouts[1].id)
    listOfScores = totals.getSingleWorkoutTotal(workout,1)

    context = {'scores' : listOfScores, 'workouts' : listOfWorkouts}
    return HttpResponse(template.render(context, request))