from django.db import models
from deschutesDemoScores.models import Score, Workout, Team

def getSingleWorkoutTotal(workout, division):
	#TODO - update to work for single workouts when fully loaded
	workoutProperties = Workout.objects.get(id = workout)
	#print(workoutProperties)
	#print(workoutProperties.scoringStyle)
	setOfScores = Score.objects.filter(workout = workoutProperties.id, team__division = division)
	#print(setOfScores[0].reps)
	#print(setOfScores[0].team.division.id)
	#TODO - eliminate some repetition in the code if possible/reasonable
	if workoutProperties.scoringStyle == 'T':
		setOfScores = sorted(setOfScores, key=lambda x: (x.minutes, x.seconds, -int(x.reps or 0)))
		listOfScores = []
		rank = 1
		for score in setOfScores:
			recordedScore = orderedScore(score, rank)
			listOfScores.append(recordedScore)
			rank += 1
		i = 0
		#tie breaks - should clean up
		for score in listOfScores:
			#print(listOfScores[i])
			isTie = False
			if i > 1:
				if listOfScores[i].score.minutes == listOfScores[i-1].score.minutes:
					if listOfScores[i].score.seconds == listOfScores[i-1].score.seconds:
						if listOfScores[i].score.reps == listOfScores[i-1].score.reps:
							isTie = True
			if isTie:
				listOfScores[i].rank = listOfScores[i-1].rank
			i += 1

	elif workoutProperties.scoringStyle == 'R':
		setOfScores = sorted(setOfScores, key=lambda x: (-int(x.reps or 0)))
		listOfScores = []
		rank = 1
		for score in setOfScores:
			recordedScore = orderedScore(score, rank)
			listOfScores.append(recordedScore)
			rank += 1
		i = 0
		for score in listOfScores:
			#print(listOfScores[i])
			isTie = False
			if i > 1:
				if listOfScores[i].score.reps == listOfScores[i-1].score.reps:
					isTie = True
			if isTie:
				listOfScores[i].rank = listOfScores[i-1].rank
			i += 1

	elif workoutProperties.scoringStyle == 'W':
		setOfScores = sorted(setOfScores, key=lambda x: (-int(x.weight or 0)))
		listOfScores = []
		rank = 1
		for score in setOfScores:
			recordedScore = orderedScore(score, rank)
			listOfScores.append(recordedScore)
			rank += 1
		i = 0
		for score in listOfScores:
			#print(listOfScores[i])
			isTie = False
			if i > 1:
				if listOfScores[i].score.weight == listOfScores[i-1].score.weight:
					isTie = True
			if isTie:
				listOfScores[i].rank = listOfScores[i-1].rank
			i += 1

	else: 
		listOfScores = []

	return listOfScores

def getAllWorkoutsTotal(division):
	setOfWorkouts = Workout.objects.filter(event = 1)
	#print(setOfWorkouts)
	listOfWorkoutScores = []
	for workout in setOfWorkouts:
		print(workout.id)
		listOfWorkoutScores.append(getSingleWorkoutTotal(workout.id,division))
	totalScores = {}
	for workout in listOfWorkoutScores:
		for score in workout:
			print(str(score.rank) + ' ' + str(score.score.team.teamID))
			if score.score.team.teamID in totalScores:
				totalScores[score.score.team.teamID] = totalScores[score.score.team.teamID] + score.rank
			else:
				totalScores[score.score.team.teamID] = score.rank
	#totalScores = sorted(totalScores.values())
	listOfTotalScores = []
	for total in totalScores:
		print(total)
		print(totalScores[total])
		listOfTotalScores.append(totalScore(totalScores[total],total))
	print(listOfTotalScores)
	#listOfTotalScores.sort(key=score)
	sortedListOfTotalScores = sorted(listOfTotalScores, key=lambda x:(x.score))
	rank = 1
	for score in sortedListOfTotalScores:
		#print(score.team + ' ' + str(score.score))
		score.rank = rank
		rank += 1
	i = 0
	for score in sortedListOfTotalScores:
		isTie = False
		if i > 1:
			if sortedListOfTotalScores[i].score == sortedListOfTotalScores[i-1].score:
				isTie = True
		if isTie:
			sortedListOfTotalScores[i].rank = sortedListOfTotalScores[i-1].rank
		i += 1
	for score in sortedListOfTotalScores:
		print(str(score.rank) + ' ' + score.team + ' ' + str(score.score))
	return sortedListOfTotalScores

class orderedScore:
	def __init__(self, score, rank):
		self.score = score
		self.rank = rank

class totalScore:
	def __init__(self, score, team):
		self.score = score
		self.team = team
		self.rank = 0