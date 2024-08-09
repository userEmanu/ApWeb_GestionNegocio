from django.shortcuts import render, redirect
from appTienda.models import Categoria, Producto
# Create your views here.

"""
Renderiza la plantilla inicio.html y devuelve la respuesta HTML renderizada.

Parameters:
    request (HttpRequest): El Objetos de solicitud HTTP.

Returns:
    HttpResponse: La respuesta del html renderizado.
"""
def inicio(request):
    return render(request,"inicio.html")

"""
Renderiza la plantilla frmCategoria.html y devuelve la respuesta HTML renderizada.

Parameters:
    request (HttpRequest): El Objetos de solicitud HTTP.

Returns:
    HttpResponse: La respuesta del html renderizado.
"""
def vistaCategorias(request):
    return render(request,"frmCategoria.html")

"""
Crea un nueva instancia del modelo Categoria y lo guarda en la base de datos.

Parameters:
    request (HttpRequest): El Objeto de solicitud HTTP que contiene los datos POST

Returns:
    HttpResponse: La respuesta HTML renderizada de la plantilla frmCategoria.html con un mensaje de éxito o error.
"""
def agregarCategoria(request):
    nombre = request.POST["txtNombre"]
    try:
        categoria = Categoria(catNombre = nombre)
        categoria.save()
        mensaje = "Categoria agregada correctamente"
    except:
        mensaje = "Problemas al agregar"
    retorno = {"mensaje": mensaje}
    return render(request, "frmCategoria.html", retorno)

def listarProductos(request):
    try: 
        productos = Producto.objects.all()
        mensaje=""
        print(productos)
    except:
        mensaje="Problemas al obtener los productos"
    retorno = {"mensaje": mensaje, "listaProductos": productos}
    return render(request, "frmListarProductos.html", retorno)

def vistaProducto(request):
    try: 
        categorias= Categoria.objects.all()
        mensaje = ""
    except: 
        mensaje = "Problemas al obtener las categorias"
    retorno = {"mensaje": mensaje, "listaCategorias": categorias, "producto": None}
    return render(request, "frmProducto.html", retorno) 

def agregarProducto(request):
    producto = None
    try:
        nombre = request.POST["txtNombre"]
        codigo = int(request.POST["txtCodigo"])
        precio = int(request.POST["txtPrecio"])
        idCategoria = int(request.POST["cbCategoria"])
        foto = request.FILES.get('fileFoto')
        categorias = Categoria.objects.get(id=idCategoria)
        
        # Crea una instancia del Producto y asigna la imagen usando la clase File
        producto = Producto(
            proNombre=nombre, 
            proCodigo=codigo, 
            proPrecio=precio,
            proCategoria=categorias,
            proFoto=foto
        )
        producto.save()
        
        mensaje = "Producto agregado correctamente"
        return redirect("/listarProductos/")
    except:
        mensaje = "Problemas al agregar el producto"
        
    categorias = Categoria.objects.all()
    retorno = {"mensaje": mensaje, "listaCategorias": categorias, "producto": producto}
    return render(request, "frmProducto.html", retorno)

def consulatarProducto(request, id):
    try:
        producto = Producto.objects.get(id = id)
        categorias = Categoria.objects.all()
        mensaje = ""
    except:
        mensaje = "Problemas al consultar, codigo incorrecto o inexistente"
    retorno = {"mensaje": mensaje,"producto": producto, "listaCategorias": categorias}
    return render(request, "frmEditarProducto.html", retorno)

def actualizarProducto(request): 
    idProducto = int(request.POST["idProducto"])
    nombre = request.POST["txtNombre"]
    codigo = int(request.POST["txtCodigo"])
    precio = int(request.POST["txtPrecio"])
    idCategoria = int(request.POST["cbCategoria"])
    archivo = request.FILES.get("fileFoto", False)
    try:
        categoria = Categoria.objects.get(id = idCategoria)
        producto = Producto.objects.get(id = idProducto)
        producto.proNombre = nombre
        producto.proPrecio = precio
        producto.proCategoria = categoria
        producto.proCodigo = codigo
        if(archivo != False):
            producto.proFoto = archivo
        producto.save()
        mensaje = "Producto actualizado correctamente"
        return redirect("/listarProductos/")
    except:
        mensaje = "Error al actualizar el producto"
    categorias = Categoria.objects.all()
    retorno = {"mensaje": mensaje, "listaCategorias": categorias, "producto": producto}
    return render(request,"frmEditarProducto.html", retorno)

def eliminarProducto(request, id):
    try: 
        producto = Producto.objects.get(id = id)
        producto.delete()
        mensaje = "Producto eliminado correctamente"
    except:
        mensje = "problema al eliminar"
    retorno = {"mensaje": mensaje}
    return redirect("/listarProductos/", retorno)