from django.db import models
from deschutesDemoScores.models import Score, Workout
import sys
import os
import csv

importFilePath = (os.path.abspath("importing/DDDemoData.csv"))
importFile = open("/Users/briano/Python/virtualenvironment/DeschutesDemo/scoring/deschutesDemoScores/importing/DDDemoData.csv")
print(importFile)

def importDDData():
	with importFile as f:
	        reader = csv.reader(f)
	        for row in reader:
	            _, created = Score.objects.get_or_create(
	                weight=row[0],
	                minutes=row[1],
	                seconds=row[2],
	                reps=row[3],
	                team=row[4],
	                workout=row[5],
	                )
	            print(row)
            # creates a tuple of the new object or
            # current object and a boolean of if it was created