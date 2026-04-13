from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Producto, Categoria
from .forms import ClienteRegistroForm


def inicio(request):
    productos_destacados = Producto.objects.filter(disponible=True, destacado=True)[:8]
    productos_nuevos = Producto.objects.filter(disponible=True)[:8]
    categorias = Categoria.objects.all()
    context = {
        'productos_destacados': productos_destacados,
        'productos_nuevos': productos_nuevos,
        'categorias': categorias,
    }
    return render(request, 'tienda/inicio.html', context)


def lista_productos(request):
    categorias = Categoria.objects.all()
    categoria_slug = request.GET.get('categoria')
    categoria_activa = None
    productos = Producto.objects.filter(disponible=True)

    if categoria_slug:
        categoria_activa = get_object_or_404(Categoria, slug=categoria_slug)
        productos = productos.filter(categoria=categoria_activa)

    busqueda = request.GET.get('q', '').strip()
    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)

    context = {
        'productos': productos,
        'categorias': categorias,
        'categoria_activa': categoria_activa,
        'busqueda': busqueda,
    }
    return render(request, 'tienda/productos.html', context)


def detalle_producto(request, slug):
    producto = get_object_or_404(Producto, slug=slug, disponible=True)
    relacionados = Producto.objects.filter(
        categoria=producto.categoria, disponible=True
    ).exclude(pk=producto.pk)[:4]
    context = {
        'producto': producto,
        'relacionados': relacionados,
    }
    return render(request, 'tienda/detalle.html', context)


def registro_cliente(request):
    if request.method == 'POST':
        form = ClienteRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'¡Bienvenido, {form.cleaned_data["nombre"]}! '
                'Te hemos registrado correctamente. Pronto nos pondremos en contacto contigo.'
            )
            return redirect('tienda:registro_exito')
    else:
        form = ClienteRegistroForm()
    return render(request, 'tienda/registro.html', {'form': form})


def registro_exito(request):
    return render(request, 'tienda/registro_exito.html')

