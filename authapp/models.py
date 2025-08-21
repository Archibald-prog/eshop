from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars',
                               verbose_name='фото', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)
