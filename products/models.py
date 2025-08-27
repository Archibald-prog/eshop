from django.db import models

from modules.services.utils import gen_slug


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=150, unique=True
    )
    slug = models.SlugField(
        max_length=160, blank=True, unique=True,
        db_index=True, verbose_name="URL"
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    category_image = models.ImageField(
        verbose_name="Изображение",
        upload_to="category_img/"
    )
    is_active = models.BooleanField(
        verbose_name="Активна",
        default=True
    )

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self, self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class ProductType(models.Model):
    name = models.CharField(
        verbose_name='Тип',
        max_length=150, unique=True
    )
    slug = models.SlugField(
        max_length=160, blank=True, unique=True,
        db_index=True, verbose_name="URL"
    )
    categories = models.ManyToManyField(
        Category, verbose_name="категории",
        related_name="category_types"
    )

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self, self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"


class Material(models.Model):
    name = models.CharField(
        verbose_name='Материал',
        max_length=150, unique=True
    )
    slug = models.SlugField(
        max_length=160, blank=True, unique=True,
        db_index=True, verbose_name="URL"
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name="Активен",
        default=True
    )

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self, self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"


class Product(models.Model):
    name = models.CharField(
        verbose_name='Товар',
        max_length=150, unique=True
    )
    slug = models.SlugField(
        max_length=160, blank=True, unique=True,
        db_index=True, verbose_name="URL"
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE
    )
    type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE
    )
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE
    )
    old_price = models.DecimalField(
        verbose_name="Старая цена",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    price = models.DecimalField(
        verbose_name="Цена",
        max_digits=8,
        decimal_places=2,
        default=0
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Количество на складе",
        default=0
    )
    is_available = models.BooleanField(
        verbose_name="Наличие в магазинах",
        default=True
    )
    is_recommended = models.BooleanField(
        verbose_name="Рекомендуемый товар",
        default=False
    )
    is_new = models.BooleanField(
        verbose_name="Новинка",
        default=False
    )
    is_hit = models.BooleanField(
        verbose_name="Хит продаж",
        default=False
    )
    is_active = models.BooleanField(
        verbose_name="Активен",
        default=True
    )

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self, self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImages(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=100
    )
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="product_images/"
    )
    product = models.ForeignKey(
        Product, verbose_name="Товар",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товара"
