from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from apps.products.models import Category, Product, Images, Faq, VideoBlog


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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'get_final_price', 'discount_percent','discount_price', 'status']
    list_filter = ('status', 'gender', 'category')
    search_fields = ('title', 'keywords')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline] 
    save_on_top = True
    fields = (
        'category', 'title', 'slug', 'gender', 'price', 'discount_percent',
        'discount_price', 'status', 'keywords', 'image', 'description'
    )

admin.site.register(Category,  CategoryAdmin) 
admin.site.register(Images)
admin.site.register(Faq)
admin.site.register(VideoBlog)