from django.db import models

class Categoria(models.Model):
    catNombre = models.CharField(max_length=50, unique = True)
    
    
class Producto(models.Model):
    proCodigo = models.IntegerField(unique = True)
    proNombre = models.CharField(max_length=50)
    proPrecio = models.IntegerField()
    proCategoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    proFoto = models.ImageField(upload_to='productos/', blank=True, null=True)
