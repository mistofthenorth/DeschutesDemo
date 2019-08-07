# Generated by Django 2.2 on 2019-08-05 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deschutesDemoScores', '0007_auto_20190709_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='athlete',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='deschutesDemoScores.Event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='score',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='deschutesDemoScores.Event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='deschutesDemoScores.Event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workout',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='deschutesDemoScores.Event'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deschutesDemoScores.Event')),
            ],
        ),
    ]