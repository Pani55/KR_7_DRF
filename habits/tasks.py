from datetime import timedelta

import requests
from celery import shared_task

from config.settings import TELEGRAM_BOT_TOKEN
from habits.models import Habit


@shared_task
def send_habit_reminder(habit_id, tg_id):
    habit = Habit.objects.get(id=habit_id)
    if habit.relation_habit:
        message = f"Пришло время выполнить {habit.action}, затем наградить себя {habit.relation_habit}"
    else:
        message = f"Пришло время выполнить {habit.action}, затем наградить себя {habit.reward}"
    params = {"text": message, "chat_id": tg_id}

    requests.get(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", params=params
    )
    habit.next_date += timedelta(days=habit.periodicity)

    send_habit_reminder.apply_async(
        (
            habit_id,
            tg_id,
        ),
        eta=habit.next_date,
    )
