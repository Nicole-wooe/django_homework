from django.contrib.auth.models import AbstractUser
from django.db import models
from users.managers import UserManager


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )
    avatar = models.ImageField(
        upload_to="users/",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        verbose_name="Телефон",
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Страна",
    )
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
