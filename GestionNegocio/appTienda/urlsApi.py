from django.urls import path
from . import apiView

urlpatterns = [
     path('CategoriaList/',apiView.categoriaList.as_view()),
     path('ProductorList/',apiView.productoList.as_view()),
     # listas Id
     path('CategoriaList/<int:pk>/',apiView.categoriaDetail.as_view()),
     path('Productor/<int:pk>/',apiView.productoId.as_view()),
     path('ProductorList/<int:proCodigo>/',apiView.productoDetail.as_view()),
     path('productoImagen/', apiView.ProductoImagen.as_view())
]