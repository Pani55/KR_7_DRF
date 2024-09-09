from datetime import timedelta

from rest_framework import serializers


def validate_duration(duration):
    try:
        duration = duration.split(":")
        if len(duration) != 2:
            raise TypeError("duration must be in MM:SS format")
        minute = duration[0]
        second = duration[1]
        duration = timedelta(minutes=int(minute), seconds=int(second))
    except TypeError as e:
        raise serializers.ValidationError(str(e))
    if duration > timedelta(minutes=2):
        raise serializers.ValidationError("Duration must be less than or equal to 2 minutes")
