from django.db import models


class Channel(models.Model):
    name = models.CharField(max_length=100)


class Performer(models.Model):
    name = models.CharField(max_length=100)


class Song(models.Model):
    title = models.CharField(max_length=100)
    namePerformer = models.ForeignKey(Performer, related_name='performer')


class Play(models.Model):
    nameSong = models.ForeignKey(Song)
    start = models.DateTimeField()
    end = models.DateTimeField()
    nameChannel = models.ForeignKey(Channel)


class TopPlayPrevious(models.Model):
    song = models.ForeignKey(Song)
    previous_plays = models.IntegerField()
    previous_rank = models.IntegerField(blank=True, null=True)


# class TopPlay(models.Model):
#    song = models.ForeignKey(Song)
#    plays = models.IntegerField(blank=True)
#    previous_plays = models.ForeignKey(TopPlayPrevious)
