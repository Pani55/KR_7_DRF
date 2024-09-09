from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="Адрес электронной почты", unique=True)
    phone = models.CharField(
        max_length=35, verbose_name="Номер телефона", blank=True, null=True
    )
    city = models.CharField(max_length=50, verbose_name="Город", blank=True, null=True)
    photo = models.ImageField(
        verbose_name="Фотография профиля", upload_to="users/", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
