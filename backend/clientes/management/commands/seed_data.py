"""
Comando de Django para poblar la base de datos con datos de prueba
Usa pandas para generar datos aleatorios
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
import pandas as pd

from clientes.models import TipoDocumento, Cliente, Compra


class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de prueba para desarrollo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clientes',
            type=int,
            default=50,
            help='Número de clientes a crear (default: 50)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando población de datos...'))
        
        # Crear tipos de documento si no existen
        tipos_doc = self._crear_tipos_documento()
        
        # Crear clientes
        num_clientes = options['clientes']
        clientes = self._crear_clientes(tipos_doc, num_clientes)
        
        # Crear compras
        self._crear_compras(clientes)
        
        # Asegurar que al menos un cliente cumpla las condiciones de fidelización
        self._crear_cliente_fidelizacion(tipos_doc)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Se crearon {len(tipos_doc)} tipos de documento'))
        self.stdout.write(self.style.SUCCESS(f'✓ Se crearon {len(clientes)} clientes'))
        self.stdout.write(self.style.SUCCESS('✓ Se crearon compras para los clientes'))
        self.stdout.write(self.style.SUCCESS('✓ Se creó al menos un cliente elegible para fidelización'))
        self.stdout.write(self.style.SUCCESS('\n¡Datos de prueba creados exitosamente!'))

    def _crear_tipos_documento(self):
        """Crea los tipos de documento si no existen"""
        tipos_data = [
            {'codigo': 'NIT', 'nombre': 'NIT', 'descripcion': 'Número de Identificación Tributaria'},
            {'codigo': 'CC', 'nombre': 'Cédula', 'descripcion': 'Cédula de Ciudadanía'},
            {'codigo': 'PA', 'nombre': 'Pasaporte', 'descripcion': 'Pasaporte'},
        ]
        
        tipos = []
        for tipo_data in tipos_data:
            tipo, created = TipoDocumento.objects.get_or_create(
                codigo=tipo_data['codigo'],
                defaults=tipo_data
            )
            tipos.append(tipo)
        
        return tipos

    def _crear_clientes(self, tipos_doc, num_clientes):
        """Crea clientes usando pandas para generar datos aleatorios"""
        # Nombres y apellidos comunes en Colombia
        nombres = [
            'Carlos', 'María', 'Juan', 'Ana', 'Luis', 'Laura', 'Pedro', 'Sofía',
            'Andrés', 'Valentina', 'Diego', 'Isabella', 'Camilo', 'Mariana',
            'Sebastián', 'Daniela', 'Javier', 'Natalia', 'Felipe', 'Andrea'
        ]
        
        apellidos = [
            'García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez',
            'Sánchez', 'Pérez', 'Gómez', 'Martín', 'Jiménez', 'Ruiz', 'Hernández',
            'Díaz', 'Moreno', 'Muñoz', 'Álvarez', 'Romero', 'Gutiérrez', 'Navarro'
        ]
        
        # Generar datos con pandas
        df_clientes = pd.DataFrame({
            'nombre': [random.choice(nombres) for _ in range(num_clientes)],
            'apellido': [random.choice(apellidos) for _ in range(num_clientes)],
            'tipo_doc': [random.choice(tipos_doc) for _ in range(num_clientes)],
        })
        
        # Generar números de documento según el tipo
        def generar_numero_doc(tipo_doc):
            if tipo_doc.codigo == 'NIT':
                return f"{random.randint(80000000, 99999999)}-{random.randint(1, 9)}"
            elif tipo_doc.codigo == 'CC':
                return str(random.randint(10000000, 99999999))
            else:  # Pasaporte
                return f"{random.choice(['AB', 'CD', 'EF', 'GH'])}{random.randint(100000, 999999)}"
        
        df_clientes['numero_doc'] = df_clientes['tipo_doc'].apply(generar_numero_doc)
        
        # Generar correos y teléfonos
        df_clientes['correo'] = df_clientes.apply(
            lambda row: f"{row['nombre'].lower()}.{row['apellido'].lower()}@email.com",
            axis=1
        )
        df_clientes['telefono'] = [
            f"3{random.randint(100000000, 999999999)}" for _ in range(num_clientes)
        ]
        
        # Crear clientes en la base de datos
        clientes = []
        for _, row in df_clientes.iterrows():
            # Verificar si el cliente ya existe
            cliente, created = Cliente.objects.get_or_create(
                tipo_documento=row['tipo_doc'],
                numero_documento=row['numero_doc'],
                defaults={
                    'nombre': row['nombre'],
                    'apellido': row['apellido'],
                    'correo': row['correo'],
                    'telefono': row['telefono'],
                }
            )
            clientes.append(cliente)
        
        return clientes

    def _crear_compras(self, clientes):
        """Crea compras aleatorias para los clientes"""
        fecha_actual = timezone.now()
        
        for cliente in clientes:
            # Cada cliente tendrá entre 1 y 10 compras
            num_compras = random.randint(1, 10)
            
            for i in range(num_compras):
                # Fechas aleatorias en los últimos 60 días
                dias_atras = random.randint(0, 60)
                fecha_compra = fecha_actual - timedelta(days=dias_atras)
                
                # Montos aleatorios entre 100.000 y 10.000.000
                monto = random.randint(100000, 10000000)
                
                numero_factura = f"FAC-{cliente.numero_documento}-{i+1:04d}"
                
                Compra.objects.get_or_create(
                    numero_factura=numero_factura,
                    defaults={
                        'cliente': cliente,
                        'fecha_compra': fecha_compra,
                        'monto': monto,
                        'descripcion': f'Compra #{i+1} del cliente',
                        'estado': random.choice(['completada', 'completada', 'completada', 'pendiente']),
                    }
                )

    def _crear_cliente_fidelizacion(self, tipos_doc):
        """Crea un cliente específico que cumpla las condiciones de fidelización"""
        # Cliente con compras superiores a 5 millones en el último mes
        tipo_doc = random.choice(tipos_doc)
        numero_doc = f"FIDEL-{random.randint(1000, 9999)}"
        
        cliente, created = Cliente.objects.get_or_create(
            tipo_documento=tipo_doc,
            numero_documento=numero_doc,
            defaults={
                'nombre': 'Cliente',
                'apellido': 'Fidelización',
                'correo': 'cliente.fidelizacion@email.com',
                'telefono': '3001234567',
            }
        )
        
        # Crear múltiples compras en el último mes que sumen más de 5 millones
        fecha_actual = timezone.now()
        monto_total = 0
        objetivo = 6000000  # 6 millones para asegurar que supere los 5
        
        compra_num = 1
        while monto_total < objetivo:
            dias_atras = random.randint(0, 30)  # Último mes
            fecha_compra = fecha_actual - timedelta(days=dias_atras)
            
            # Monto entre 500.000 y 2.000.000
            monto = random.randint(500000, 2000000)
            
            if monto_total + monto > objetivo:
                monto = objetivo - monto_total + random.randint(100000, 500000)
            
            numero_factura = f"FAC-FIDEL-{compra_num:04d}"
            
            Compra.objects.get_or_create(
                numero_factura=numero_factura,
                defaults={
                    'cliente': cliente,
                    'fecha_compra': fecha_compra,
                    'monto': monto,
                    'descripcion': f'Compra de fidelización #{compra_num}',
                    'estado': 'completada',
                }
            )
            
            monto_total += monto
            compra_num += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'  Cliente fidelización creado: {cliente.numero_documento} '
                f'(Total compras: ${monto_total:,.2f} COP)'
            )
        )

