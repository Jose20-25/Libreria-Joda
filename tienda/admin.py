from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Producto, Cliente

admin.site.site_header = 'Librería Joda — Panel Administrativo'
admin.site.site_title = 'Librería Joda Admin'
admin.site.index_title = 'Administración de la Tienda'


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'vista_previa_imagen')
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ('nombre',)

    def vista_previa_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.imagen.url)
        return '—'
    vista_previa_imagen.short_description = 'Imagen'


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'vista_previa_imagen', 'nombre', 'categoria', 'precio',
        'precio_oferta', 'stock', 'disponible', 'destacado', 'creado'
    )
    list_display_links = ('vista_previa_imagen', 'nombre')
    list_filter = ('disponible', 'destacado', 'categoria')
    list_editable = ('disponible', 'destacado', 'stock', 'precio')
    search_fields = ('nombre', 'descripcion')
    prepopulated_fields = {'slug': ('nombre',)}
    readonly_fields = ('creado', 'actualizado', 'vista_previa_imagen')
    ordering = ('-creado',)
    list_per_page = 20

    fieldsets = (
        ('Información Principal', {
            'fields': ('nombre', 'slug', 'categoria', 'descripcion')
        }),
        ('Imagen', {
            'fields': ('imagen', 'vista_previa_imagen')
        }),
        ('Precios e Inventario', {
            'fields': ('precio', 'precio_oferta', 'stock')
        }),
        ('Estado', {
            'fields': ('disponible', 'destacado')
        }),
        ('Fechas', {
            'fields': ('creado', 'actualizado'),
            'classes': ('collapse',)
        }),
    )

    def vista_previa_imagen(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="height:50px;width:50px;object-fit:cover;border-radius:4px;" />',
                obj.imagen.url
            )
        return format_html('<span style="color:#aaa;">Sin imagen</span>')
    vista_previa_imagen.short_description = 'Vista previa'


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'registrado', 'contactar_whatsapp')
    search_fields = ('nombre', 'telefono')
    readonly_fields = ('registrado',)
    ordering = ('-registrado',)
    list_per_page = 25

    def contactar_whatsapp(self, obj):
        numero = ''.join(filter(str.isdigit, obj.telefono))
        if numero:
            url = f'https://wa.me/52{numero}?text=Hola%20{obj.nombre},%20te%20contactamos%20desde%20Librer%C3%ADa%20Joda.'
            return format_html(
                '<a href="{}" target="_blank" style="color:#25D366;font-weight:600;">'
                '<img src="https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/whatsapp.svg" '
                'style="height:16px;margin-right:4px;filter:invert(49%) sepia(85%) saturate(400%) hue-rotate(100deg);">'
                'WhatsApp</a>',
                url
            )
        return '—'
    contactar_whatsapp.short_description = 'Contactar'

