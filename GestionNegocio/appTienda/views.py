from django.shortcuts import render, redirect
from appTienda.models import Categoria, Producto
from django.core.exceptions import ValidationError
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
    nombre = request.POST.get("txtNombre", "").strip() # Obtener el valor del campo requirido, si esta vacio de vuelve una cadena vacia, 
    # strip elimina los espacios al final y principio
    if not nombre: # verifica que no este vacio
        mensaje = "Debe indicar el nombre de la categoria"
        retorno = {"mensaje": mensaje}
        return render(request, "frmCategoria.html", retorno)
    # Verifica que no exista la categoria con el mismo nombre para impedir la duplicidad de datos
    if Categoria.objects.filter(catNombre=nombre).exists():
        mensaje = "La categoria ya existe"
        retorno = {"mensaje": mensaje}
        return render(request, "frmCategoria.html", retorno)
    # si todo esta correcto, procede a crear la instancia de la categoria y guardar
    try: 
        categoria = Categoria(catNombre = nombre)
        categoria.full_clean() # Valida el modelo antes de guardar.
        categoria.save()
        mensaje = "Categoria agregada correctamente"
    except ValidationError as error: 
        print(error, "Error de validacion")
        mensaje = "Error de validación: Por favor, revise los datos ingresados."
    except Exception as error:
        print(error, "Problemas Al agregar")
        mensaje = "Problemas al agregar: Por favor, intente más tarde."
    retorno = {"mensaje": mensaje}
    return render(request, "frmCategoria.html", retorno)

"""
Recupera todos lo datos de los productos de la base de datos en una lista y renderiza la plantilla de html para
mostrar los datos.

Parameters:
    request (HttpRequest):  El objeto de solicitud HTTP que contiene los datos de la solicitud.

Returns:
    HttpResponse: La plantilla HTML renderizada con una lista de productos y un mensaje.
"""
def listarProductos(request):
    try: 
        productos = Producto.objects.all() # recupera todos los datos de los productos en la base de datos
    except Exception as error:
        mensaje="Porfavor intente mas tarde"
    retorno = {"mensaje": mensaje, "listaProductos": productos}
    return render(request, "frmListarProductos.html", retorno)
"""
Recupera todas las categorias de la base de datos y renderiza la plantilla 'frmProducto.html' con las categorias y un mensaje.

Parameters:
    request (HttpRequest): El objeto de solicitud HTTP que contiene los datos de la solicitud.

Returns:
    HttpResponse: Renderiza la plantilla 'frmProducto.html' con las categorias y un mensaje. 
"""
def vistaProducto(request):
    try: 
        categorias= Categoria.objects.all()
    except: 
        mensaje = "Problemas al obtener las categorias"
    retorno = {"mensaje": mensaje, "listaCategorias": categorias}
    return render(request, "frmProducto.html", retorno) 

"""
Agrega un producto a la base de datos basado en los datos recibidos en la solicitud.

Args:
    request (HttpRequest): El objeto de solicitud HTTP.

Returns:
    HttpResponse: Se renderizada la plantilla HTML  con el producto agregado exitosamente o un mensaje de error.

Raises:
    ValidationError: Si los datos del producto no pasan la validación.
    Exception: Si hay un problema al agregar el producto.
"""
def agregarProducto(request):
    nombre = request.POST.get("txtNombre", "").strip()
    codigo = request.POST.get("txtCodigo", "").strip()
    precio = request.POST("txtPrecio", "").strip()
    idCategoria = request.POST.get("cbCategoria", "").strip()
    foto = request.FILES.get('fileFoto')
    
    if not all[(nombre, codigo, precio, idCategoria)]: # verifica las variables no esten vacias
        mensaje = "Todos los campos son obligatorios"
        categorias = Categoria.objects.all()
        return render(request, "frmProducto.html", {"mensaje": mensaje, "listaCategorias": categorias})
    
    if Producto.objects.filter(proCodigo=int(codigo)).exists(): # verifica que no exista un producto con el mismo Codigo
        mensaje = "Ya existe un producto con el mismo Codigo"
        categorias = Producto.objects.all()
        return render(request, "frmProducto.html", {"mensaje": mensaje, "listaCategorias": categorias})
    
    try:
        categorias = Categoria.objects.get(id=int(idCategoria))
        producto = Producto(
            proNombre=nombre, 
            proCodigo= int(codigo), 
            proPrecio=int(precio),
            proCategoria=categorias,
            proFoto=foto
        )
        producto.full_clean() # Valida el modelo antes de guardar.
        producto.save()
        mensaje = "Producto agregado correctamente"
    except ValidationError as error:
        print(error, "Error de validacion")
        mensaje = "Error de validación: Por favor, revise los datos ingresados."
    except Exception as error:
        print(error, "Problemas Al agregar")
        mensaje = "Problemas al agregar: Por favor, intente más tarde."
        
    categorias = Categoria.objects.all()
    retorno = {"mensaje": mensaje, "listaCategorias": categorias}
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