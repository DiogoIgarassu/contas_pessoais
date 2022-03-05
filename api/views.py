from rest_framework import viewsets
from django.contrib.auth.models import User
from api.serializers import UserSerializer, CreditoSerializer
from credito.models import Compras


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreditoViewSet(viewsets.ModelViewSet):
    queryset = Compras.objects.all()
    serializer_class = CreditoSerializer

