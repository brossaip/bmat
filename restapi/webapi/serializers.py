from rest_framework import serializers
from webapi.models import Channel, Performer, Song, Play


class ChannelSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):
        return Channel.objects.create(**validated_data)


class PerformerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Performer
        fields = ('name')


class SongSerializer(serializers.Serializer):
    title = serializers.CharField()
    performer = serializers.CharField()

    def create(self, validated_data):
        perf = Performer(name=validated_data.get('performer'))
        song = Song(title=validated_data.get('title'), namePerformer=perf)
        return song


class PlaySerializer(serializers.Serializer):
    title = serializers.CharField()
    performer = serializers.CharField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    channel = serializers.CharField()

    def create(self, validated_data):
        perf = Performer(name=validated_data.get('performer'))
        song = Song(title=validated_data.get('title'), namePerformer=perf)
        chan = Channel(name=validated_data.get('performer'))
        start = validated_data.get('start')
        end = validated_data.get('end')
        play = Play(nameSong=song, start=start, end=end, nameChannel=chan)
        return play


class PlaySongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = ('nameChannel', 'start', 'end')
