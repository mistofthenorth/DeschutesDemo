from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Team, Score, Workout, Division
from .totaling import totals
from .importing import DDDataImport


def index(request):
    try:
        #print(request.POST['workout'])
        #print(request.POST['division'])
        workout = request.POST['workout']
        division = request.POST['division']
    except:
        #print('no post available')
        workout = 6
        division = 1
    #print('workout number is ' + str(workout))
    template = loader.get_template('scoring/index.html')
    #DDDataImport.importDDTeams()
    #DDDataImport.importDDData()
    listOfWorkouts = Workout.objects.filter(event = 1)
    listOfDivisions = Division.objects.filter(event = 1)
    #print(listOfWorkouts[1].id)
    listOfScores = totals.getSingleWorkoutTotal(workout,division)
    scoringStyle = Workout.objects.get(pk=workout)
    #print(scoringStyle.scoringStyle)
    #
    allWorkouts = totals.getAllWorkoutsTotal(1)
    #print(listOfWorkouts[0][0].rank)
    #
    context = {'scores' : listOfScores, 'workouts' : listOfWorkouts, 'divisions' : listOfDivisions, 'scoringStyle' : scoringStyle.scoringStyle}
    return HttpResponse(template.render(context, request))