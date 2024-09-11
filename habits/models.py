from datetime import timedelta

from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        blank=True,
        null=True,
    )
    place = models.CharField(
        max_length=100, verbose_name="Место выполнения", blank=True, null=True
    )
    time = models.TimeField(verbose_name="Время выполнения", blank=True, null=True)
    action = models.CharField(
        max_length=200, verbose_name="Действие", blank=True, null=True
    )
    is_pleasant = models.BooleanField(
        verbose_name="Признак приятной привычки", default=False
    )
    relation_habit = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        verbose_name="Связанная привычка",
        blank=True,
        null=True,
    )
    reward = models.CharField(
        max_length=200,
        verbose_name="Награда за выполнение привычки",
        blank=True,
        null=True,
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность выполнения привычки в днях",
        blank=True,
    )
    action_duration = models.CharField(
        max_length=50,
        default=timedelta(minutes=2),
        verbose_name="Продолжительность выполнения действия",
        blank=True,
    )
    is_public = models.BooleanField(
        verbose_name="Публичная привычка", default=False, blank=True
    )
    first_date = models.DateTimeField(
        verbose_name="Дата первого выполнения",
        blank=True,
        null=True,
    )
    next_date = models.DateTimeField(
        verbose_name="Дата следующего выполнения",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"{self.user} - {self.action}"
