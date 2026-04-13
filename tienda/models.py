from django.db import models
from django.utils.text import slugify


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='productos', verbose_name='Categoría'
    )
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    precio_oferta = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name='Precio de oferta'
    )
    stock = models.PositiveIntegerField(default=0, verbose_name='Stock')
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, verbose_name='Imagen')
    disponible = models.BooleanField(default=True, verbose_name='Disponible')
    destacado = models.BooleanField(default=False, verbose_name='Destacado')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-creado']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nombre)
            slug = base_slug
            n = 1
            while Producto.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def precio_final(self):
        return self.precio_oferta if self.precio_oferta else self.precio

    @property
    def tiene_oferta(self):
        return self.precio_oferta is not None and self.precio_oferta < self.precio

