from django.db import models
from deschutesDemoScores.models import Score, Workout, Team, Event

def getSingleWorkoutTotal(workout, division):

	workoutProperties = Workout.objects.get(id = workout)
	setOfTeams = Team.objects.filter(division = division)
	setOfScores = Score.objects.filter(workout = workoutProperties.id, team__division = division)

	if workoutProperties.scoringStyle == 'T':
		setOfScores = sorted(setOfScores, key=lambda x: ((x.minutes or float('inf')), (x.seconds or float('inf')), -int(x.reps or 0)))
	elif workoutProperties.scoringStyle == 'R':
		setOfScores = sorted(setOfScores, key=lambda x: (-int(x.reps or 0)))
	elif workoutProperties.scoringStyle == 'W':
		setOfScores = sorted(setOfScores, key=lambda x: (-int(x.weight or 0)))
	else:
		pass
	#Add blank entries for teams that have no scores on this workout
	teamIDList = [x.teamID for x in setOfTeams]
	scoreTeamIDList = [x.team.teamID for x in setOfScores]
	missingTeamsList = set(teamIDList) - set(scoreTeamIDList)

	for team in missingTeamsList:
		(blankScore, created) = Score.objects.get_or_create(weight = None, minutes = None, seconds = None, reps = None, team=Team.objects.get(pk=team), workout=Workout.objects.get(pk=workout), event=Event.objects.get(pk=1))
		setOfScores.append(blankScore)

	listOfScores = []
	for (rank, score) in enumerate(setOfScores, 1):
		recordedScore = orderedScore(score, rank)
		listOfScores.append(recordedScore)

	for (i, score) in enumerate(listOfScores):
		isTie = False
		if i == 0: continue # Don't run this check on the first item since no tie is possible with previous score
		#print(listOfScores[i].score.team)
		#print(listOfScores[i].score.minutes) 
		if workoutProperties.scoringStyle == 'T':
			if (listOfScores[i].score.minutes or float('inf')) == (listOfScores[i-1].score.minutes or float('inf')) and (listOfScores[i].score.seconds or float('inf')) == (listOfScores[i-1].score.seconds or float('inf')) and (listOfScores[i].score.reps or 0) == (listOfScores[i-1].score.reps or 0):
				isTie = True
		elif workoutProperties.scoringStyle == 'R':
			if (listOfScores[i].score.reps or 0) == (listOfScores[i-1].score.reps or 0) and (listOfScores[i].score.minutes or 0) == (listOfScores[i-1].score.minutes or 0) and (listOfScores[i].score.seconds or 0) == (listOfScores[i-1].score.seconds or 0):
				isTie = True
		elif workoutProperties.scoringStyle == 'W':
			if (listOfScores[i].score.weight or 0) == (listOfScores[i-1].score.weight or 0) and (listOfScores[i].score.minutes or 0) == (listOfScores[i-1].score.minutes or 0) and (listOfScores[i].score.seconds or 0) == (listOfScores[i-1].score.seconds or 0):
				isTie = True
		else:
			isTie = False

		if isTie:
			listOfScores[i].rank = listOfScores[i-1].rank

	return listOfScores

def getAllWorkoutsTotal(division):

	setOfWorkouts = Workout.objects.filter(event = 1)

	listOfWorkoutScores = []
	for workout in setOfWorkouts:
		if workout.includeInFinalResults:
			listOfWorkoutScores.append(getSingleWorkoutTotal(workout.id,division))

	allEventScores = {}
	totalScores = {}
	for workout in listOfWorkoutScores:
		for score in workout:
			if score.score.team.teamID in totalScores:
				totalScores[score.score.team.teamID] = totalScores[score.score.team.teamID] + score.rank
				allEventScores[score.score.team.teamID].append(score)
				#print(allEventScores[score.score.team.teamID])
			else:
				totalScores[score.score.team.teamID] = score.rank
				allEventScores[score.score.team.teamID] = [score]
				#print(allEventScores[score.score.team.teamID])


	listOfTotalScores = []
	for total in totalScores:
		listOfTotalScores.append(totalScore(totalScores[total],total,allEventScores[total]))

	sortedListOfTotalScores = sorted(listOfTotalScores, key=lambda x:(x.score))

	for (rank,score) in enumerate(sortedListOfTotalScores, 1):
		score.rank = rank

	for (i, score) in enumerate(sortedListOfTotalScores):
		if i == 0: continue
		
		if sortedListOfTotalScores[i].score == sortedListOfTotalScores[i-1].score:
			sortedListOfTotalScores[i].rank = sortedListOfTotalScores[i-1].rank

	#for score in sortedListOfTotalScores:
		#print(str(score.rank) + ' ' + score.team + ' ' + str(score.score))

	return (sortedListOfTotalScores, listOfWorkoutScores)

class orderedScore:
	def __init__(self, score, rank):
		self.score = score
		self.rank = rank

class totalScore:
	def __init__(self, score, team, eventScores):
		self.score = score
		self.team = team
		self.rank = 0
		self.eventScores = eventScores