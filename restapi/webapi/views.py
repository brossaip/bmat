from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from webapi.models import Channel, Performer, Song, Play
from webapi.serializers import ChannelSerializer, PerformerSerializer, SongSerializer, PlaySerializer


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
        if serializer.is_valid():
            perf = Performer.objects.get_or_create(
                name=serializer.validated_data.get('performer'))
            song = Song.objects.get_or_create(
                title=serializer.validated_data.get('title'),
                namePerformer=perf)
            chan = Channel.objects.get_or_create(
                name=serializer.validated_data.get('performer'))
            start = serializer.validated_data.get('start')
            end = serializer.validated_data.get('end')
            play = Play(nameSong=song, start=start, end=end, nameChannel=chan)
            play.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
