from django.contrib import admin
from .models import TipoDocumento, Cliente, Compra


@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['codigo', 'nombre']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['numero_documento', 'nombre_completo', 'correo', 'telefono', 'fecha_registro', 'activo']
    list_filter = ['tipo_documento', 'activo', 'fecha_registro']
    search_fields = ['numero_documento', 'nombre', 'apellido', 'correo']
    readonly_fields = ['fecha_registro']


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['numero_factura', 'cliente', 'fecha_compra', 'monto', 'estado']
    list_filter = ['estado', 'fecha_compra']
    search_fields = ['numero_factura', 'cliente__nombre', 'cliente__apellido', 'cliente__numero_documento']
    date_hierarchy = 'fecha_compra'

