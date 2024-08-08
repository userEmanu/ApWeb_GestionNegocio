from rest_framework import serializers
from appTienda.models import *
from drf_extra_fields.fields import Base64ImageField

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Categoria
        fields = ('__all__')

class ProductoSerializer(serializers.ModelSerializer):
    proFoto = Base64ImageField(required = False)
    class Meta: 
        model = Producto
        fields = ('__all__')

