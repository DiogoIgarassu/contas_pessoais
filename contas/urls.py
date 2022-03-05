"""contas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from credito.views import fatura,add_compra, edit_compra, del_compra

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fatura', fatura, name="fatura"),
    path('edit_compra/<int:pk>/', edit_compra, name="edit_compra"),
    path('del_compra/<int:pk>/', del_compra, name="del_compra"),
    path('add_compra', add_compra, name="add_compra")
]
