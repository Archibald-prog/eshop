from django.db import models


class Contact(models.Model):
    city = models.CharField(
        verbose_name="город",
        max_length=128
    )
    phone = models.CharField(
        verbose_name="телефон",
        max_length=64
    )
    email = models.CharField(
        verbose_name="email",
        max_length=64
    )
    address = models.CharField(
        verbose_name="адрес",
        max_length=128
    )

    def __str__(self):
        return (f"{self.city} {self.phone} "
                f"{self.email} {self.address}")

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"

