from django.db import models
from django.conf import settings
from products.models import Product


class BasketQueryset(models.QuerySet):
    def total_price(self):
        return sum(basket.product_cost for basket in self)

    def total_quantity(self):
        if self:
            return sum(basket.quantity for basket in self)
        return 0

    def shipping_price(self):
        if self:
            if self.total_price() > 10000:
                return 600
            return 400
        else:
            return 0


class Basket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='basket'
    )
    session_key = models.CharField(
        max_length=32,
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        default=0
    )
    add_datetime = models.DateTimeField(
        verbose_name='Время добавления',
        auto_now_add=True
    )

    objects = BasketQueryset().as_manager()

    def __str__(self):
        if self.user:
            return (f'Корзина {self.user.username} | '
                    f'Товар {self.product.name} | '
                    f'Количество {self.quantity}')
        return (f'Анонимная корзина | '
                f'Товар {self.product.name} | '
                f'Количество {self.quantity}')

    @property
    def product_cost(self):
        return round(self.product.price * self.quantity, 2)
