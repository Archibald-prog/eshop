from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars',
                               verbose_name='фото', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
