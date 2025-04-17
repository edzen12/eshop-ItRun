from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from apps.products.views import (home, product_detail, 
                                category_detail, contact, search_view)
from apps.users.views import login_view, reg_view, logout_view, profile_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('register/', reg_view, name='register'),
    path('search/', search_view, name='search'),
]
urlpatterns += i18n_patterns(
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('profile/', profile_view, name='profile'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('category/<slug:slug>/', category_detail, name='category_detail'),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
