from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from apps.products import views
from apps.users.views import (login_view, reg_view, logout_view, profile_view)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('register/', reg_view, name='register'),
    path('search/', views.search_view, name='search'),
    path('checkout/', views.checkout_view, name='checkout'),
]
urlpatterns += i18n_patterns(
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('profile/', profile_view, name='profile'),
    path('products/male/', views.male_products, name='male_products'),
    path('products/female/', views.female_products, name='female_products'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('faq/', views.faq, name='faq'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('vlog/', views.vlog, name='vlog'),
    path('discount-products/', views.discount_products, name='discount_products'),

    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/add/ajax/', views.cart_add_ajax, name='cart_add_ajax'),
    path('cart/remove/ajax/', views.cart_remove_ajax, name='cart_remove_ajax'),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
