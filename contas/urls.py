from django.contrib import admin
from django.urls import path, include
from credito.views import fatura,add_compra, edit_compra, del_compra, dashboard
from api.views import UserViewSet, CreditoViewSet
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import get_schema_view


schema_view = get_swagger_view(title='Pastebin API')
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'credito', CreditoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("docs/", schema_view, name='docs'),
    path('admin/', admin.site.urls),
    path('fatura', fatura, name="fatura"),
    path('dashboard', dashboard, name="dashboard"),
    path('edit_compra/<str:pk>/', edit_compra, name="edit_compra"),
    path('del_compra/<str:pk>/', del_compra, name="del_compra"),
    path('add_compra', add_compra, name="add_compra"),
    path('api-auth/', include('rest_framework.urls')),
    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
]


