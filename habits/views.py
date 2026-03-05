from django_celery_beat.models import PeriodicTask
from rest_framework import generics

from habits.models import Habit
from habits.paginators import HabitsPagination
from habits.serializers import HabitsSerializer, PublicHabitsSerializer
from habits.services import set_schedule
from users.permissions import IsOwner


class HabitCreateAPIView(generics.CreateAPIView):
    """Создание привычки."""

    serializer_class = HabitsSerializer
    permission_classes = (IsOwner,)

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)
        self._update_habit(habit)

    def _update_habit(self, habit):
        if not habit.is_pleasant:
            habit.save()

            if habit.user.chat_id:
                set_schedule(habit)


class PublicHabitListAPIView(generics.ListAPIView):
    """Публичные привычки."""

    serializer_class = PublicHabitsSerializer

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitListAPIView(generics.ListAPIView):
    """Список привычек пользователя."""

    serializer_class = HabitsSerializer
    pagination_class = HabitsPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Детальная информация о привычке."""

    queryset = Habit.objects.all()
    serializer_class = HabitsSerializer
    permission_classes = (IsOwner,)


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Обновление привычки."""

    queryset = Habit.objects.all()
    serializer_class = HabitsSerializer
    permission_classes = (IsOwner,)

    def perform_update(self, serializer):
        habit = serializer.save(user=self.request.user)
        habit.refresh_from_db()
        if not habit.is_pleasant and habit.user.chat_id:
            PeriodicTask.objects.filter(name=f"Habit Task - {habit.id}").delete()
            set_schedule(habit)


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Удаление привычки."""

    queryset = Habit.objects.all()
    serializer_class = HabitsSerializer
    permission_classes = (IsOwner,)
