from django.contrib import admin
from appTienda.models import Producto, Categoria
# Registrar los modelos a los cuales puede acceder el Admin de django
admin.site.register(Categoria)
admin.site.register(Producto)