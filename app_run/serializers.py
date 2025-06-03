from django.contrib.auth.models import User
from rest_framework import serializers
import urllib.parse
from django.shortcuts import get_object_or_404
import json

from .models import AthleteInfo, Run, Challenge, Position, CollectibleItem, Subscriber


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
    runs_finished = serializers.IntegerField(read_only=True)

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


class AthleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = AthleteInfo
        fields = "__all__"


class ChallengeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Challenge
        fields = "__all__"


class PositionSerializer(serializers.ModelSerializer):
    date_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%f")

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
        fields = [
            "name",
            "uid",
            "latitude",
            "longitude",
            "picture",
            "value",
        ]

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
        
class UserItemsSerializer(UserSerializer): 
    items = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields + ['items']
        
    def get_items(self, obj):
        items = CollectibleItem.objects.filter(items=obj)
        return CollectibleItemSerializer(items, many=True).data
    
class UserCoachSerializer(UserItemsSerializer): 
    athletes = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = UserItemsSerializer.Meta.fields + ['athletes']
        
    def get_athletes(self, obj):
        athletes = Subscriber.objects.filter(coach=obj.id)
        return (athlete_id for athlete_id in list(athletes.values_list('athlete', flat=True)))


class UserAthleteSerializer(UserItemsSerializer): 
    coach = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = UserItemsSerializer.Meta.fields + ['coach']
        
    def get_coach(self, obj):
        coach = Subscriber.objects.filter(athlete=obj.id).first()
        return coach.coach.id if coach else []
    
    
class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ["coach", "athlete"]
        
    def validate(self, data):
        if data["coach"] == data["athlete"]:
            raise serializers.ValidationError("Пользователи не могут быть подписаны сами на себя.")
        double_subscribe = Subscriber.objects.filter(coach=data["coach"], athlete=data["athlete"]).count()
        if double_subscribe:
            raise serializers.ValidationError("Подписка уже оформлена.")
        user_ = get_object_or_404(User, id=data["athlete"].id)
        if user_.is_staff:
            raise serializers.ValidationError("Подписываться могут только пользователи с типом 'athlete'")
        return data