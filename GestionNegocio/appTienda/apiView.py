from rest_framework import generics
from appTienda.models import Categoria, Producto
from appTienda.serializers import CategoriaSerializer, ProductoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Serializa el modelo de Categoria a JSON
class categoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# Serializa el modelo de Producto a JSON 
class productoList(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

# Permite recuperar(GET), actualizar(PUT/PATCH) y eliminar(DELETE) instancias del modelo categoria
# La informacion se serializa a JSON, tanto la que resive o devuelve
class categoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# Permite recuperar(GET), actualizar(PUT/PATCH) y eliminar(DELETE) instancia del modelo Producto, solamente si coincide con el campo "proCodigo"
# La informacion se serializa a JSON, tanto la que resive o devuelve
class productoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    lookup_field = 'proCodigo'

# Permite recuperar(GET), actualizar(PUT/PATCH) y eliminar(DELETE) instancias del modelo producto
# La informacion se serializa a JSON, tanto la que resive o devuelve
class productoId(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

# Permite subir una imagen al servidor serializada en base64.
# El método POST recibe los datos del producto, valida y guarda la imagen y los datos del producto.
class ProductoImagen(APIView):
    def post(self,request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            archivo = validated_data['proFoto']
            archivo.name = 'producto.png'
            validated_data['proFoto'] = archivo
            producto = Producto(**validated_data)
            producto.save()
            serializer_response = ProductoSerializer(producto)
            return Response(serializer_response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)