# Generated by Django 4.1.2 on 2022-10-30 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oparser', '0002_alter_product_options_product_currency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='published_date',
            field=models.DateTimeField(verbose_name='Publication date'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='currency',
            field=models.TextField(blank=True, null=True, verbose_name='Currency'),
        ),
    ]
