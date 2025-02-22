# Generated by Django 4.2.18 on 2025-01-16 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AlterField(
            model_name='category',
            name='status',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], default='True', max_length=10),
        ),
    ]
