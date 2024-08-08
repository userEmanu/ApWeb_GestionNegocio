from rest_framework import generics
from appTienda.models import Categoria, Producto
from appTienda.serializers import CategoriaSerializer, ProductoSerializer
from django.http import JsonResponse
from django.core import serializers
from django.contrib import auth
from django.http import HttpResponse
import json
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Listas

class categoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    

class productoList(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class categoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
 
class productoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    lookup_field = 'proCodigo'
    
class productoId(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
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