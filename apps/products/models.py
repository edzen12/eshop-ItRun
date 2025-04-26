from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey


class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey(
        'self', blank=True, null=True, 
        related_name='children', on_delete=models.CASCADE
    )
    title = models.CharField(max_length=50, verbose_name="Название категории")
    keywords = models.CharField(max_length=255, verbose_name="ключевые слова для категории")
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS,default='True')
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'категория'

class Product(models.Model):
    STATUS = (
        ('True', 'True'), # в наличии товар
        ('False', 'False'), # нет товара
    )
    GENDER_CHOICES = (
        ('male', 'Мужское'),
        ('female', 'Женское'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="категории")
    title = models.CharField(max_length=50, verbose_name="Название")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True, verbose_name="Пол")
    price = models.DecimalField(verbose_name='цена',max_digits=12, decimal_places=2, default=0)
    discount_price = models.DecimalField(
        verbose_name="Фиксированная скидка (в валюте)",
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="Например: -500 означает скидку  500 сомов" 
    )  
    discount_percent = models.PositiveIntegerField(
        verbose_name="Процентная скидка (%)",
        blank=True, null=True, 
        help_text="Например: 20 означает скидку 20%"
    )
    keywords = models.CharField(max_length=255, verbose_name="ключевые слова для товара")
    image = models.ImageField(blank=True, upload_to='images/')
    description = models.TextField(verbose_name="Описание")
    status = models.CharField(max_length=10, choices=STATUS, default='True')
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
    
    def get_final_price(self):
        price = self.price
        
        # если есть процентная скидка
        if self.discount_percent:
            price = price - (price * self.discount_percent/ 100)

        # если есть фиксированная скидка
        if self.discount_price:
            price = price - self.discount_price

        return max(price, 0)

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'товар'


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, null=True)
    img = models.ImageField(blank=True, upload_to='product-detail')

    def __str__(self):
        return self.product.title



class Comment(models.Model):
    STATUS = (
        ('New', 'New'), # Новый
        ('True', 'True'), # Публикованные
        ('False', 'False'), # Не публикованный
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="ФИО")
    email = models.CharField(max_length=155)
    comment = models.TextField()
    rate = models.IntegerField(default=1)
    status = models.CharField(choices=STATUS, default='New', max_length=10)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.email



class Faq(models.Model):
    title = models.CharField(max_length=100, verbose_name="Вопрос")
    description = models.TextField(verbose_name="Ответ")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Вопросы/Ответы'
        verbose_name = 'вопрос/ответ'