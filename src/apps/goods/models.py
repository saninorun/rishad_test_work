from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from pytils.translit import slugify


class Product(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ("id",)

    def __str__(self):
        return f'{self.title} Количество - {self.quantity}'

    def display_id(self):
        return f"{self.id:05}"

    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'product_slug': self.slug})
    def save(self, *args, **kwargs):
        """
        Дополнение родительского метода сохранения модели в базу данных,
        в случае отсутствия значения переменной 'slug' при заполнении поля модели.
        """

        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
