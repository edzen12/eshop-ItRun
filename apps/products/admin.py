from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from apps.products.models import Category, Product, Images


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = 'title'
    list_display = ('tree_actions','indented_title', 'status')
    mptt_level_indent = 50
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}


class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'price']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]

admin.site.register(Category,  CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images)