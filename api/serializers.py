from rest_framework import serializers

class TimeSerializer(serializers.Serializer):
    now = serializers.JSONField()

class ElapsedSerializer(serializers.Serializer):
    now = serializers.JSONField()
    elapsed = serializers.JSONField()