from django.db import models
from deschutesDemoScores.models import Score

def getSingleWorkoutTotal():
	#TODO - update to work for single workouts when fully loaded
	setOfScores = Score.objects.all()
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
		print(listOfScores[i])
		isTie = False
		if i > 1:
			if listOfScores[i].score.minutes == listOfScores[i-1].score.minutes:
				if listOfScores[i].score.seconds == listOfScores[i-1].score.seconds:
					if listOfScores[i].score.reps == listOfScores[i-1].score.reps:
						isTie = True
		if isTie:
			listOfScores[i].rank = listOfScores[i-1].rank
		i += 1

	return listOfScores

class orderedScore:

	def __init__(self, score, rank):
		self.score = score
		self.rank = rank
