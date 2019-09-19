from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Team, Score, Workout, Division, Event
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
    #allWorkouts = totals.getAllWorkoutsTotal(1)
    #print(listOfWorkouts[0][0].rank)
    #
    context = {'scores' : listOfScores, 'workouts' : listOfWorkouts, 'divisions' : listOfDivisions, 'scoringStyle' : scoringStyle.scoringStyle}
    return HttpResponse(template.render(context, request))


def finalResults(request):
    try:
        #print(request.POST['workout'])
        #print(request.POST['division'])
        division = request.POST['division']
    except:
        #print('no post available')
        division = 1
    listOfDivisions = Division.objects.filter(event = 1)
    allWorkouts = totals.getAllWorkoutsTotal(division)
    #print(allWorkouts[1])
    #print(allWorkouts[0][0].rank)
    template = loader.get_template('scoring/finalResults.html')
    context = {'divisions' : listOfDivisions, 'allWorkouts' : allWorkouts[0], 'workoutScores' : allWorkouts[1]}
    return HttpResponse(template.render(context, request))

def scoreInput(request):
    try:
        #print(request.POST['workout'])
        #print(request.POST['division'])
        workout = request.POST['workout']
        division = request.POST['division']
    except:
        #print('no post available')
        workout = 6
        division = 1
    setOfTeams = Team.objects.filter(division = division)
    listOfScores = totals.getSingleWorkoutTotal(workout,division)
    sortedListOfScores = sorted(listOfScores, key=lambda x: (x.score.team_id))
    template = loader.get_template('scoring/scoreInput.html')
    context = {'setOfTeams' : setOfTeams, 'scores' : sortedListOfScores}
    return HttpResponse(template.render(context, request))

def scoreInputReceived(request):
    print(request.POST)
    try:
        #print(request.POST['workout'])
        #print(request.POST['division'])
        workout = request.POST['workout']
        division = request.POST['division']
    except:
        #print('no post available')
        workout = 6
        division = 1
    listOfTeams = request.POST.getlist('team')
    listOfMinutes = request.POST.getlist('minutes')
    listOfSeconds = request.POST.getlist('seconds')
    listOfWeight = request.POST.getlist('weight')
    listOfReps = request.POST.getlist('reps')
    for (i, teamScore) in enumerate(listOfTeams):
        score = Score.objects.get(team=listOfTeams[i],workout=workout,event=1)
        score.weight = listOfWeight[i]
        score.reps = listOfReps[i]
        score.minutes = listOfMinutes[i]
        score.seconds = listOfSeconds[i]
        score.save()
        print(score)
        
        #except:
        #    print('unable to write row to database ' + str(i))

    #for i in request.POST:
    #    print(i)
    template = loader.get_template('scoring/scoreInputReceived.html')
    context = {}
    return HttpResponse(template.render(context, request))
