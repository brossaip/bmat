from django.db import models
import numpy


class Channel(models.Model):
    name = models.CharField(max_length=100)


class Performer(models.Model):
    name = models.CharField(max_length=100)


class Song(models.Model):
    title = models.CharField(max_length=100)
    namePerformer = models.ForeignKey(Performer)
    previous_ranking = models.PositiveIntegerField(
        default=numpy.exp2(31))  # By default it is the maximum integer
    previous_plays = models.PositiveIntegerField(
        default=numpy.exp2(31))


class Play(models.Model):
    nameSong = models.ForeignKey(Song)
    start = models.DateTimeField()
    end = models.DateTimeField()
    nameChannel = models.ForeignKey(Channel)
