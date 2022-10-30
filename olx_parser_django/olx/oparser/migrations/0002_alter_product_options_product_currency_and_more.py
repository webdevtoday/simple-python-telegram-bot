# Generated by Django 4.1.2 on 2022-10-30 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oparser', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AddField(
            model_name='product',
            name='currency',
            field=models.TextField(default='₴', verbose_name='Currency'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='url',
            field=models.URLField(unique=True, verbose_name='Link to ad'),
        ),
    ]
