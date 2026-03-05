import json

from django_celery_beat.models import CrontabSchedule, PeriodicTask


def set_schedule(habit):
    """Создание расписания для напоминаний о привычке."""

    schedule, created = CrontabSchedule.objects.get_or_create(
        minute=habit.time.minute,
        hour=habit.time.hour,
        day_of_month=f"*/{habit.period}",
        month_of_year="*",
        day_of_week="*",
    )
    task_name = f"Habit Task - {habit.id}"

    # Удаляем старую задачу с таким же именем
    PeriodicTask.objects.filter(name=task_name).delete()

    PeriodicTask.objects.create(
        crontab=schedule,
        name=task_name,
        task="habits.tasks.send_message",
        args=json.dumps([habit.id]),
        one_off=False,  # Задача повторяется по расписанию
        start_time=habit.created_at,  # Начинаем с момента создания
    )
