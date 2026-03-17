from rest_framework import serializers
from bson import ObjectId

from .models import Activity, LeaderboardEntry, Team, User, Workout


class ObjectIdField(serializers.Field):
    """Custom field to handle MongoDB ObjectId serialization"""

    def to_representation(self, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value

    def to_internal_value(self, data):
        if isinstance(data, str) and len(data) == 24:
            try:
                return ObjectId(data)
            except:
                pass
        return data


class TeamSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)

    class Meta:
        model = Team
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)

    class Meta:
        model = Activity
        fields = '__all__'


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)

    class Meta:
        model = LeaderboardEntry
        fields = '__all__'


class WorkoutSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)

    class Meta:
        model = Workout
        fields = '__all__'
