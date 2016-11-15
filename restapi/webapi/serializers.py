from rest_framework import serializers
from webapi.models import Channel, Performer, Song, Play


class ChannelSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):
        return Channel.objects.create(**validated_data)


class PerformerSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):
        return Performer.objects.create(**validated_data)


class SongSerializer(serializers.Serializer):
    title = serializers.CharField()
    performer = PerformerSerializer()
    previous_ranking = serializers.IntegerField()
    previous_plays = serializers.IntegerField()

    def create(self, validated_data):
        return Song.objects.create(**validated_data)


class PlaySerializer(serializers.Serializer):
    nameSong = SongSerializer()
    nameChannel = ChannelSerializer()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()

    def create(self, validated_data):
        return Play.objects.create(**validated_data)
