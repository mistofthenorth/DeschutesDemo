from django.db import models

class Event(models.Model):
	description = models.CharField(max_length=100)

class Workout(models.Model):
	description = models.CharField(max_length=100)
	reps = models.IntegerField()
	scoringStyle = (
					('W', 'weight'),
					('R', 'reps'),
					('T', 'time'))

class Team(models.Model):
	description = models.CharField(max_length=100)

class Athlete(models.Model):
	description = models.CharField(max_length=100)
	tems = models.IntegerField()

class Score(models.Model):
	weight = models.IntegerField()
	minutes = models.IntegerField()
	seconds = models.IntegerField()
	reps = models.IntegerField()
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.team.description) + ' ' + str(self.workout.description)
    
