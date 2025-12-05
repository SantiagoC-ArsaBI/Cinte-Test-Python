# Backend - Sistema de Consulta de Clientes

API REST desarrollada con Django y Django REST Framework.

## Estructura

```
backend/
├── config/              # Configuración de Django
│   ├── settings.py      # Configuración principal
│   ├── urls.py          # URLs principales
│   └── wsgi.py          # WSGI config
├── clientes/            # Aplicación de clientes
│   ├── models.py        # Modelos: TipoDocumento, Cliente, Compra
│   ├── views.py         # ViewSets y endpoints de API
│   ├── serializers.py   # Serializadores REST
│   ├── urls.py          # URLs de la aplicación
│   ├── admin.py         # Configuración del admin
│   └── management/       # Comandos personalizados
│       └── commands/
│           └── seed_data.py  # Comando para poblar BD
├── manage.py            # Script de gestión de Django
└── requirements.txt     # Dependencias
```

## Endpoints de la API

### Base URL: `http://localhost:8000/api/`

- `GET /api/tipos-documento/` - Lista tipos de documento
- `GET /api/clientes/` - Lista clientes
- `GET /api/clientes/{id}/` - Detalles de cliente
- `GET /api/clientes/buscar/?tipo_documento_id={id}&numero_documento={num}` - Buscar cliente
- `GET /api/clientes/{id}/exportar/?formato={csv|excel|txt}` - Exportar cliente
- `GET /api/reporte-fidelizacion/generar/` - Generar reporte de fidelización

## Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Poblar base de datos
python manage.py seed_data --clientes 50

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver

# Acceder al admin
# http://localhost:8000/admin/
```

## Modelos

### TipoDocumento
- Código único (NIT, CC, PA)
- Nombre y descripción

### Cliente
- Tipo y número de documento (único)
- Nombre, apellido, correo, teléfono
- Relación con TipoDocumento

### Compra
- Cliente (ForeignKey)
- Número de factura (único)
- Fecha, monto, descripción, estado

## Base de Datos

Por defecto usa SQLite (`db.sqlite3`). Para producción, se recomienda usar PostgreSQL o MySQL.

