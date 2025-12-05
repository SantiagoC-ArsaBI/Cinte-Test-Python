from django.db import models
from django.core.validators import EmailValidator
from django.utils import timezone
from datetime import timedelta


class TipoDocumento(models.Model):
    """Modelo para tipos de documento (NIT, Cédula, Pasaporte)"""
    codigo = models.CharField(max_length=10, unique=True, verbose_name="Código")
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    """Modelo para información básica del cliente"""
    tipo_documento = models.ForeignKey(
        TipoDocumento,
        on_delete=models.PROTECT,
        related_name='clientes',
        verbose_name="Tipo de Documento"
    )
    numero_documento = models.CharField(max_length=50, unique=True, verbose_name="Número de Documento")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    correo = models.EmailField(
        max_length=255,
        validators=[EmailValidator()],
        verbose_name="Correo Electrónico"
    )
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['apellido', 'nombre']
        unique_together = [['tipo_documento', 'numero_documento']]
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.numero_documento}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"


class Compra(models.Model):
    """Modelo para las compras asociadas a cada cliente"""
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='compras',
        verbose_name="Cliente"
    )
    numero_factura = models.CharField(max_length=50, unique=True, verbose_name="Número de Factura")
    fecha_compra = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Compra")
    monto = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Monto (COP)"
    )
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('completada', 'Completada'),
            ('cancelada', 'Cancelada'),
        ],
        default='completada',
        verbose_name="Estado"
    )
    
    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ['-fecha_compra']
        indexes = [
            models.Index(fields=['cliente', '-fecha_compra']),
            models.Index(fields=['-fecha_compra']),
        ]
    
    def __str__(self):
        return f"Factura {self.numero_factura} - {self.cliente.nombre_completo} - ${self.monto:,.2f}"

