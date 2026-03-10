import requests
from celery import shared_task

from config.settings import TELEGRAM_BOT_TOKEN
from habits.models import Habit


@shared_task
def send_message(habit_id) -> None:
    """Функция напоминания пользователю."""

    habit = Habit.objects.get(id=habit_id)

    text = f"Трекер привычек напоминает: " f"{habit.action} в {habit.time} в/на {habit.place}"
    params = {
        "text": text,
        "chat_id": habit.user.chat_id,
    }
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", params=params)
