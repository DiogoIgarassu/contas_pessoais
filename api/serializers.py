from rest_framework import serializers
from django.contrib.auth.models import User
from credito.models import Compras


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class CreditoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Compras
        fields = '__all__'