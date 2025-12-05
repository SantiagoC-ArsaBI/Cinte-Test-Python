from rest_framework import serializers
from .models import TipoDocumento, Cliente, Compra


class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = ['id', 'codigo', 'nombre', 'descripcion']


class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = ['id', 'numero_factura', 'fecha_compra', 'monto', 'descripcion', 'estado']


class ClienteSerializer(serializers.ModelSerializer):
    tipo_documento = TipoDocumentoSerializer(read_only=True)
    tipo_documento_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoDocumento.objects.filter(activo=True),
        source='tipo_documento',
        write_only=True
    )
    compras = CompraSerializer(many=True, read_only=True)
    nombre_completo = serializers.ReadOnlyField()
    
    class Meta:
        model = Cliente
        fields = [
            'id',
            'tipo_documento',
            'tipo_documento_id',
            'numero_documento',
            'nombre',
            'apellido',
            'nombre_completo',
            'correo',
            'telefono',
            'fecha_registro',
            'activo',
            'compras'
        ]
        read_only_fields = ['fecha_registro']


class ClienteBusquedaSerializer(serializers.ModelSerializer):
    """Serializer simplificado para búsqueda de cliente"""
    tipo_documento = TipoDocumentoSerializer(read_only=True)
    nombre_completo = serializers.ReadOnlyField()
    total_compras = serializers.SerializerMethodField()
    compras = CompraSerializer(many=True, read_only=True)
    monto_total_compras = serializers.SerializerMethodField()
    
    class Meta:
        model = Cliente
        fields = [
            'id',
            'tipo_documento',
            'numero_documento',
            'nombre',
            'apellido',
            'nombre_completo',
            'correo',
            'telefono',
            'fecha_registro',
            'total_compras',
            'compras',
            'monto_total_compras'
        ]
    
    def get_total_compras(self, obj):
        """Calcula el total de compras del cliente"""
        return obj.compras.filter(estado='completada').count()
    
    def get_monto_total_compras(self, obj):
        """Calcula el monto total de compras completadas"""
        from django.db.models import Sum
        total = obj.compras.filter(estado='completada').aggregate(
            total=Sum('monto')
        )['total'] or 0
        return float(total)

