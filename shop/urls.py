"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views as app_views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app_views.home, name='home'),
    path('product/<int:id>',app_views.product, name='product-detail'),
    path('category/', app_views.category_view, name='category'),
    path('cart/', app_views.cart, name='cart'),
    path('login/', app_views.login_view, name='login'),
    path('logout/', app_views.logout_view, name='logout'),
    path('order/', app_views.order_view, name='order')
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns = urlpatterns +\
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
