from django.db import models
from deschutesDemoScores.models import Score, Workout, Team

def getSingleWorkoutTotal(workout, division):

	workoutProperties = Workout.objects.get(id = workout)
	setOfScores = Score.objects.filter(workout = workoutProperties.id, team__division = division)

	if workoutProperties.scoringStyle == 'T':
		setOfScores = sorted(setOfScores, key=lambda x: (x.minutes, x.seconds, -int(x.reps or 0)))
	elif workoutProperties.scoringStyle == 'R':
		setOfScores = sorted(setOfScores, key=lambda x: (-int(x.reps or 0)))
	elif workoutProperties.scoringStyle == 'W':
		setOfScores = sorted(setOfScores, key=lambda x: (-int(x.weight or 0)))
	else:
		pass

	listOfScores = []
	for (rank, score) in enumerate(setOfScores):
		recordedScore = orderedScore(score, rank + 1)
		listOfScores.append(recordedScore)

	for (i, score) in enumerate(listOfScores):
		isTie = False
		if i == 0: continue # Don't run this check on the first item since no tie is possible with previous score

		if workoutProperties.scoringStyle == 'T':
			if listOfScores[i].score.minutes == listOfScores[i-1].score.minutes and listOfScores[i].score.seconds == listOfScores[i-1].score.seconds and listOfScores[i].score.reps == listOfScores[i-1].score.reps:
				isTie = True
		elif workoutProperties.scoringStyle == 'R':
			if listOfScores[i].score.reps == listOfScores[i-1].score.reps and (listOfScores[i].score.minutes or 0) == (listOfScores[i-1].score.minutes or 0) and (listOfScores[i].score.seconds or 0) == (listOfScores[i-1].score.seconds or 0):
				isTie = True
		elif workoutProperties.scoringStyle == 'W':
			if listOfScores[i].score.weight == listOfScores[i-1].score.weight and (listOfScores[i].score.minutes or 0) == (listOfScores[i-1].score.minutes or 0) and (listOfScores[i].score.seconds or 0) == (listOfScores[i-1].score.seconds or 0):
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

	totalScores = {}
	for workout in listOfWorkoutScores:
		for score in workout:
			if score.score.team.teamID in totalScores:
				totalScores[score.score.team.teamID] = totalScores[score.score.team.teamID] + score.rank
			else:
				totalScores[score.score.team.teamID] = score.rank

	listOfTotalScores = []
	for total in totalScores:
		listOfTotalScores.append(totalScore(totalScores[total],total))

	sortedListOfTotalScores = sorted(listOfTotalScores, key=lambda x:(x.score))

	for (rank,score) in enumerate(sortedListOfTotalScores):
		score.rank = rank + 1

	for (i, score) in enumerate(sortedListOfTotalScores):
		if i == 0: continue
		
		if sortedListOfTotalScores[i].score == sortedListOfTotalScores[i-1].score:
			sortedListOfTotalScores[i].rank = sortedListOfTotalScores[i-1].rank

	for score in sortedListOfTotalScores:
		print(str(score.rank) + ' ' + score.team + ' ' + str(score.score))

	return (sortedListOfTotalScores, listOfWorkoutScores)

class orderedScore:
	def __init__(self, score, rank):
		self.score = score
		self.rank = rank

class totalScore:
	def __init__(self, score, team):
		self.score = score
		self.team = team
		self.rank = 0