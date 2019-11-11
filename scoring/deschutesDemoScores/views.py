from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Team, Score, Workout, Division, Event
from .totaling import totals
from .importing import DDDataImport


def index(request):
    try:
        workout = request.POST['workout']
        division = request.POST['division']
    except:
        workout = 1
        division = 1
    template = loader.get_template('scoring/index.html')
    #DDDataImport.importDDTeams()
    #DDDataImport.importDDData()
    print(workout)
    print(division)
    listOfWorkouts = Workout.objects.filter(event=1)
    listOfDivisions = Division.objects.filter(event=1)
    listOfScores = totals.getSingleWorkoutTotal(workout, division)
    scoringStyle = Workout.objects.get(pk=workout)
    context = {'scores': listOfScores, 'workouts': listOfWorkouts, 'divisions': listOfDivisions,
               'scoringStyle': scoringStyle.scoringStyle, 'currentDivision': int(division), 'currentWorkout': int(workout)}
    return HttpResponse(template.render(context, request))


def finalResults(request):
    try:
        division = request.POST['division']
    except:
        division = 1

    currentDivision = Division.objects.get(pk=division)
    currentDivisionDescription = currentDivision.description
    listOfDivisions = Division.objects.filter(event=1)
    listOfWorkouts = Workout.objects.filter(event=1)
    allWorkouts = totals.getAllWorkoutsTotal(division)
    template = loader.get_template('scoring/finalResults.html')
    context = {'divisions': listOfDivisions, 'allWorkouts': allWorkouts,
               'workouts': listOfWorkouts, 'currentDivision': currentDivisionDescription}
    return HttpResponse(template.render(context, request))


@login_required
def scoreInput(request):
    try:
        workout = request.POST['workout']
        division = request.POST['division']
    except:
        workout = 1
        division = 1

    listOfScores = totals.getSingleWorkoutTotal(workout, division)
    sortedListOfScores = sorted(listOfScores, key=lambda x: (x.score.team_id))
    template = loader.get_template('scoring/scoreInput.html')
    context = {'scores': sortedListOfScores}
    return HttpResponse(template.render(context, request))


def scoreInputReceived(request):
    print(request.POST)
    try:
        workout = request.POST['workout']
        division = request.POST['division']
    except:
        workout = 1
        division = 1
    # Split into lists
    listOfTeams = request.POST.getlist('team')
    listOfMinutes = request.POST.getlist('minutes')
    listOfSeconds = request.POST.getlist('seconds')
    listOfWeight = request.POST.getlist('weight')
    listOfReps = request.POST.getlist('reps')
    listOfSaveResults = []

    for (i, teamScore) in enumerate(listOfTeams):
        score = Score.objects.get(
            team=listOfTeams[i], workout=workout, event=1)
        score.weight = listOfWeight[i]
        score.reps = listOfReps[i]
        score.minutes = listOfMinutes[i]
        score.seconds = listOfSeconds[i]
        try:
            score.save()
            listOfSaveResults.append('Updated score for team ' + listOfTeams[i] + ' to ' + str(score.minutes) + ' minutes, ' + str(
                score.seconds) + ' seconds, ' + str(score.reps) + ' reps and ' + str(score.weight) + ' weight')
        except:
            listOfSaveResults.append(
                'unable to save score for team ' + listOfTeams[i])

    template = loader.get_template('scoring/scoreInputReceived.html')
    context = {'listOfSaveResults': listOfSaveResults}
    return HttpResponse(template.render(context, request))
