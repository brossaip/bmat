from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection

from webapi.models import Channel, Performer, Song, Play, TopPlayPrevious
from webapi.serializers import ChannelSerializer, PerformerSerializer
from webapi.serializers import SongSerializer, PlaySerializer, PlaySongSerializer

import datetime


@api_view(['POST'])
def add_channel(request):
    if request.method == 'POST':
        serializer = ChannelSerializer(data=request.data)
        if serializer.is_valid():
            # Comprovar que no existeixi (304 Not modified)
            obj, created = Channel.objects.get_or_create(
                name=serializer.validated_data['name'])
            if created:
                serializer.save()
                print("New object stored in DB")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("Object already in DB")
                return Response(serializer.data, status=status.HTTP_304_NOT_MODIFIED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_performer(request):
    if request.method == 'POST':
        serializer = PerfomerSerializer(data=request.data)
        if serializer.is_valid():
            obj, created = Performer.objects.get_or_create(
                name=serializer.validated_data['name'])
            if created:
                serializer.save()
                print("New object stored in DB")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("Object already in DB")
                return Response(serializer.data, status=status.HTTP_304_NOT_MODIFIED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_song(request):
    if request.method == 'POST':
        print(request.data)
        serializer = SongSerializer(data=request.data)
        # print(repr(serializer))
        if serializer.is_valid():
            perfobj, created = Performer.objects.get_or_create(
                name=serializer.validated_data.get('performer'))
            if created:
                perfobj.save()
                print("New performer stored in DB")
            else:
                print("Performer already in DB")
            songobj, created = Song.objects.get_or_create(
                title=serializer.validated_data.get('title'),
                namePerformer=perfobj)
            if created:
                songobj.save()
                print("New song stored in DB")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("Song already in DB")
                return Response(serializer.data, status=status.HTTP_304_NOT_MODIFIED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_play(request):
    if request.method == 'POST':
        serializer = PlaySerializer(data=request.data)
        error = False
        if serializer.is_valid():
            perf, created = Performer.objects.get_or_create(
                name=serializer.validated_data.get('performer'))
            if created:
                print("Performance not in the system")
                error = True
            song, created = Song.objects.get_or_create(
                title=serializer.validated_data.get('title'),
                namePerformer=perf.id)
            if created:
                print("Song not in the system")
                error = True
            chan, created = Channel.objects.get_or_create(
                name=serializer.validated_data.get('channel'))
            if created:
                print("Channel not in the system")
                error = True
            if error:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                start = serializer.validated_data.get('start')
                end = serializer.validated_data.get('end')
                play = Play(nameSong=song, start=start, end=end, nameChannel=chan)
                play.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_song_plays(request, title, performer, start, end):
    if request.method == 'GET':
        print('title: ' + title + '; perf:' + performer + '; start: ' + start +
              '; end: ' + end)
        perf = Performer.objects.filter(name=performer).get()
        song = Song.objects.filter(title=title, namePerformer=perf).get()
        plays = Play.objects.filter(nameSong=song,
                                    start__gte=start,
                                    start__lte=end).all()
        # Only songs that have started in this time period
        print("Quants trobats: " + str(len(plays)))
        return_data = []
        for play in plays:
            data_seri = {'nameChannel': play.nameChannel.name,
                         'start': str(play.start),
                         'end': str(play.end)}
            return_data.append(str(data_seri))
        return Response(return_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_channel_plays(request, channel, start, end):
    if request.method == 'GET':
        print('channel: ' + channel + '; start: ' + start +
              '; end: ' + end)
        chan = Channel.objects.filter(name=channel).get()
        plays = Play.objects.filter(nameChannel=chan,
                                    start__gte=start,
                                    start__lte=end).all()
        # Only songs that have started in this time period
        print("Quants trobats: " + str(len(plays)))
        return_data = []
        for play in plays:
            data_seri = {'performer': play.nameSong.namePerformer.name,
                         'title': play.nameSong.title,
                         'start': str(play.start),
                         'end': str(play.end)}
            return_data.append(str(data_seri))
        return Response(return_data, status=status.HTTP_200_OK)


# Assumptions: - channel is only one, not an array.
#              - start indicates the start of the week
#              - As before, only songs started during the parameter start plus one week
@api_view(['GET'])
def get_top(request, channel, start, limit):
    if request.method == 'GET':
        print('channel: ' + channel + '; start: ' + start +
              '; limit: ' + limit)
        # - The songs played during that week are listed.
        # - The number of plays of that week are aggregated
        # - Fill the field previous_plays
        # - Fill the field previous_ranks
        # - Serialize the top limit songs.
        TopPlayPrevious.objects.all().delete()
        start_plusweek = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S') \
            + datetime.timedelta(weeks=1)
        start_minusweek = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S') \
            - datetime.timedelta(weeks=1)
        chan = Channel.objects.filter(name=channel).get()
        # Songs played during previous week
        # After much time looking in pages to use filters in aggregation in django
        # I have used a raw query for less complexity
        query = "select nameSong_id,count(nameSong_id) as quantes from webapi_play where " + \
                "start>='" + str(start_minusweek) + "' and start<='" + start + "'" + \
                " and nameChannel_id = " + str(chan.id) + \
            " group by nameSong_id order by quantes desc"
        cur = connection.cursor()
        songsprevious = cur.execute(query).fetchall()
        ranking = 1
        for playsong in songsprevious:
            song = Song.objects.filter(id=playsong[0]).get()

            TopPlayPrevious(song=song,
                            previous_plays=playsong[1],
                            previous_rank=ranking
                            ).save()
            ranking = ranking + 1

        # Songs played during searched week
        # Prepare the data to return
        query = "select nameSong_id,count(nameSong_id) as quantes " + \
                "from webapi_play where start>='" + start + "' and start<='" + \
                str(start_plusweek) + "'" + "and nameChannel_id = " + str(chan.id) + \
                " group by nameSong_id order by quantes desc"
        cur = connection.cursor()
        songs = cur.execute(query).fetchall()
        return_data = []
        ranking = 1
        for playsong in songs:
            print("TopPlay - playsong: " + str(playsong))
            song = Song.objects.filter(id=playsong[0]).get()
            try:
                tpp = TopPlayPrevious.objects.filter(song=song).get()
                if tpp.previous_rank <= limit:
                    prev_plays = tpp.previous_plays
                    prev_rank = tpp.previous_rank
                    plays = str(playsong[1])
                else:
                    prev_plays = 0
                    prev_rank = None
                    plays = 0
            except TopPlayPrevious.DoesNotExist:
                prev_plays = 0
                prev_rank = None
                plays = 0

            data_seri = {'performer': song.namePerformer.name,
                         'title': song.title,
                         'plays': plays,
                         'previous_plays': str(prev_plays),
                         'rank': str(ranking),
                         'previous_rank': str(prev_rank)}
            return_data.append(str(data_seri))
            ranking = ranking + 1
            if ranking > limit:
                break
        return Response(return_data, status=status.HTTP_200_OK)
