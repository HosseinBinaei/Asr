from rest_framework import serializers


class TimeSerializer(serializers.Serializer):
    time = serializers.CharField()

class ElapsedSerializer(serializers.Serializer):
    value = serializers.CharField()

class DateTrackerSerializer(serializers.Serializer):
    date_tracker = serializers.CharField()