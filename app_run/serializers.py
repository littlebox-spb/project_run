from django.contrib.auth.models import User
from rest_framework import serializers
import urllib.parse

from .models import AthleteInfo, Run, Challenge, Position, CollectibleItem


class RunAthleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "last_name", "first_name"]


class RunSerializer(serializers.ModelSerializer):
    athlete_data = RunAthleteSerializer(source="athlete", read_only=True)

    class Meta:
        model = Run
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "date_joined",
            "username",
            "last_name",
            "first_name",
            "type",
            "runs_finished",
        ]

    def get_type(self, obj):
        return "coach" if obj.is_staff else "athlete"

    def get_runs_finished(self, obj):
        return User.objects.filter(run__status="finished", id=obj.id).count()


class AthleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = AthleteInfo
        fields = "__all__"


class ChallengeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Challenge
        fields = "__all__"


class PositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Position
        fields = "__all__"

    def validate_run(self, value):
        if value.status != "in_progress":
            raise serializers.ValidationError("Забег должен быть в статусе 'in_progress'")
        else:
            return value 

    def validate_latitude(self, value):
        try:
            value = float(value)
        except ValueError:
            raise serializers.ValidationError("Широта должна быть числом.")
        if -90.0 <= value <= 90.0:
            return round(value,4)
        raise serializers.ValidationError("Широта должна находиться в диапазоне от -90.0 до +90.0 градусов.")

    def validate_longitude(self, value):
        try:
            value = float(value)
        except ValueError:
            raise serializers.ValidationError("Долгота должна быть числом.")
        if -180.0 <= value <= 180.0:
            return round(value,4)
        raise serializers.ValidationError("Долгота должна находиться в диапазоне от -180.0 до +180.0 градусов.")

class CollectibleItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CollectibleItem
        fields = '__all__'

    def validate_name(self, value):
        if value:
            return value
        raise serializers.ValidationError("Название должно быть задано.")

    def validate_latitude(self, value):
        try:
            value = float(value)
        except ValueError:
            raise serializers.ValidationError("Широта должна быть числом.")
        if -90.0 <= value <= 90.0:
            return round(value,4)
        raise serializers.ValidationError("Широта должна находиться в диапазоне от -90.0 до +90.0 градусов.")

    def validate_longitude(self, value):
        try:
            value = float(value)
        except ValueError:
            raise serializers.ValidationError("Долгота должна быть числом.")
        if -180.0 <= value <= 180.0:
            return round(value,4)
        raise serializers.ValidationError("Долгота должна находиться в диапазоне от -180.0 до +180.0 градусов.")

    def validate_picture(self, value):
        try:
            result = urllib.parse.urlparse(value)
            return value
        except ValueError:
            raise serializers.ValidationError("Некорректный URL-адрес.")
        if all([result.scheme, result.netloc]):
            return value
        else:            
            raise serializers.ValidationError("Некорректный URL-адрес.")