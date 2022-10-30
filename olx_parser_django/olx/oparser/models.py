from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.TextField(
        verbose_name='Header',
    )
    price = models.PositiveIntegerField(
        verbose_name='Price',
    )
    currency = models.TextField(
        verbose_name='Currency',
        null=True,
        blank=True,
    )
    url = models.URLField(
        verbose_name='Link to ad',
        unique=True,
    )
    published_date = models.DateTimeField(
        verbose_name='Publication date',
    )

    def __str__(self):
        return f'#{self.pk} {self.title}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
