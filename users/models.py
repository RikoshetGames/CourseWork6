from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    verify_code = models.CharField(max_length=12, verbose_name='код верификации', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активный')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


