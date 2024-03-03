from django.db import models

from apps.goods.models import Product


class CartQuerySet(models.QuerySet):
    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    session_key = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = 'Cart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    objects = CartQuerySet().as_manager()

    def products_price(self):
        return round(self.product.price * self.quantity, 2)

    def __str__(self) -> str:
        return f'Товар {self.product.title} | Количество {self.quantity}'
