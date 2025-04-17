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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="категории")
    title = models.CharField(max_length=50, verbose_name="Название")
    price = models.DecimalField(verbose_name='цена',max_digits=12, decimal_places=2, default=0)
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