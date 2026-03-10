from rest_framework import serializers

from habits.models import Habit
from habits.validators import HabitValidator


class HabitsSerializer(serializers.ModelSerializer):

    time = serializers.TimeField(
        format="%H:%M", input_formats=["%H:%M"], help_text="Время начала выполнения (ЧЧ:ММ)", required=True
    )
    time_success = serializers.IntegerField(
        min_value=1, max_value=120, help_text="Время выполнения в секундах (не более 120)", required=True
    )

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]
        validators = [HabitValidator()]

    def to_internal_value(self, data):
        if self.instance and self.partial:
            return data
        return super().to_internal_value(data)


class PublicHabitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = ("action", "is_pleasant", "time_success")
