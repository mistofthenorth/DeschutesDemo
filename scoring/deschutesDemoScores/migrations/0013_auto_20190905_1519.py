# Generated by Django 2.2 on 2019-09-05 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deschutesDemoScores', '0012_workout_includeinfinalresults'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='score',
            unique_together={('team', 'workout', 'event')},
        ),
    ]