from django.db import models

class Event(models.Model):
	description = models.CharField(max_length=100)
	def __str__(self):
		return self.description

class Workout(models.Model):
	description = models.CharField(max_length=100)
	reps = models.IntegerField()
	scoringStyleChoices = (
					('W', 'weight'),
					('R', 'reps'),
					('T', 'time'),)
	scoringStyle = models.CharField(
		max_length=1,
		choices=scoringStyleChoices,
		default='T')
	def __str__(self):
		return self.description

class Team(models.Model):
	description = models.CharField(max_length=100)
	def __str__(self):
		return self.description

class Athlete(models.Model):
	description = models.CharField(max_length=100)
	teams = models.IntegerField()
	def __str__(self):
		return self.description

class Score(models.Model):
	weight = models.IntegerField()
	minutes = models.IntegerField()
	seconds = models.IntegerField()
	reps = models.IntegerField()
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.team.description) + ' ' + str(self.workout.description)
    
