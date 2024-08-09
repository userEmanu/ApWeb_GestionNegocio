from rest_framework import serializers
from appTienda.models import *
from drf_extra_fields.fields import Base64ImageField

# Convierte instancias del modelo Categoria a JSON, lo que permite enviar los datos del modelo atra vez de una API
# convierte datos json recibidos en instancias del modelo categoria, permitiendo crear o actualizar registros de la base de datos
# Los campos fields = ('__all__') indica todos los campos, como tambien puede indicarse ciertos campos
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Categoria
        fields = ('__all__')


class ProductoSerializer(serializers.ModelSerializer):
    proFoto = Base64ImageField(required = False)
    # El campo Profoto: Especifica que se puede manejar las imagenes codificadas en base64. 
    # El resquired = False, indica que el campo es opcional.
    class Meta: 
        model = Producto
        fields = ('__all__')

