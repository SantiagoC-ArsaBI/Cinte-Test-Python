# Documentación Técnica - Sistema de Consulta de Clientes

## Arquitectura del Sistema

El sistema está compuesto por dos partes principales:

1. **Backend**: API REST desarrollada con Django y Django REST Framework
2. **Frontend**: Aplicación web desarrollada con React

### Diagrama de Arquitectura

```
┌─────────────┐
│   React     │  Frontend (Puerto 3000)
│  Frontend   │
└──────┬──────┘
       │ HTTP/REST
       │
┌──────▼──────┐
│   Django    │  Backend (Puerto 8000)
│   REST API  │
└──────┬──────┘
       │
┌──────▼──────┐
│  SQLite     │  Base de Datos
│  Database   │
└─────────────┘
```

## Modelo de Datos

### Entidades Principales

#### 1. TipoDocumento
Representa los tipos de documento de identificación.

**Campos:**
- `id`: Identificador único (PK)
- `codigo`: Código único del tipo (NIT, CC, PA)
- `nombre`: Nombre del tipo (NIT, Cédula, Pasaporte)
- `descripcion`: Descripción del tipo
- `activo`: Estado activo/inactivo

#### 2. Cliente
Representa la información básica del cliente.

**Campos:**
- `id`: Identificador único (PK)
- `tipo_documento`: Relación ForeignKey con TipoDocumento
- `numero_documento`: Número de documento (único)
- `nombre`: Nombre del cliente
- `apellido`: Apellido del cliente
- `correo`: Correo electrónico
- `telefono`: Número de teléfono
- `fecha_registro`: Fecha de registro automática
- `activo`: Estado activo/inactivo

**Índices:**
- Índice único compuesto: `(tipo_documento, numero_documento)`

#### 3. Compra
Representa las compras realizadas por los clientes.

**Campos:**
- `id`: Identificador único (PK)
- `cliente`: Relación ForeignKey con Cliente
- `numero_factura`: Número de factura (único)
- `fecha_compra`: Fecha de la compra
- `monto`: Monto de la compra en COP
- `descripcion`: Descripción de la compra
- `estado`: Estado (pendiente, completada, cancelada)

**Índices:**
- Índice compuesto: `(cliente, -fecha_compra)`
- Índice: `(-fecha_compra)`

### Relaciones

```
TipoDocumento (1) ──< (N) Cliente
Cliente (1) ──< (N) Compra
```

## API REST - Endpoints

### Base URL
```
http://localhost:8000/api/
```

### 1. Tipos de Documento

#### GET /api/tipos-documento/
Obtiene la lista de tipos de documento activos.

**Respuesta:**
```json
[
  {
    "id": 1,
    "codigo": "CC",
    "nombre": "Cédula",
    "descripcion": "Cédula de Ciudadanía"
  }
]
```

### 2. Clientes

#### GET /api/clientes/
Obtiene la lista de clientes (con paginación).

#### GET /api/clientes/{id}/
Obtiene los detalles de un cliente específico.

**Respuesta:**
```json
{
  "id": 1,
  "tipo_documento": {
    "id": 1,
    "codigo": "CC",
    "nombre": "Cédula"
  },
  "numero_documento": "12345678",
  "nombre": "Juan",
  "apellido": "Pérez",
  "nombre_completo": "Juan Pérez",
  "correo": "juan.perez@email.com",
  "telefono": "3001234567",
  "fecha_registro": "2024-01-01T10:00:00Z",
  "activo": true,
  "compras": [...]
}
```

#### GET /api/clientes/buscar/?tipo_documento_id={id}&numero_documento={numero}
Busca un cliente por tipo y número de documento.

**Parámetros:**
- `tipo_documento_id` (requerido): ID del tipo de documento
- `numero_documento` (requerido): Número de documento

**Respuesta:**
```json
{
  "id": 1,
  "tipo_documento": {...},
  "numero_documento": "12345678",
  "nombre": "Juan",
  "apellido": "Pérez",
  "nombre_completo": "Juan Pérez",
  "correo": "juan.perez@email.com",
  "telefono": "3001234567",
  "fecha_registro": "2024-01-01T10:00:00Z",
  "total_compras": 5
}
```

#### GET /api/clientes/{id}/exportar/?formato={csv|excel|txt}
Exporta la información del cliente en el formato especificado.

**Parámetros:**
- `formato` (opcional): csv, excel o txt (default: csv)

**Respuesta:** Archivo descargable

### 3. Reporte de Fidelización

#### GET /api/reporte-fidelizacion/generar/
Genera un reporte en Excel con clientes elegibles para fidelización.

**Criterios:**
- Compras en el último mes (30 días)
- Monto total de compras >= $5'000.000 COP
- Estado de compras: completada

**Respuesta:** Archivo Excel (.xlsx) descargable

**Estructura del Excel:**
- Columnas: Tipo Documento, Número Documento, Nombre, Apellido, Correo, Teléfono, Total Compras (COP)
- Ordenado por Total Compras descendente

## Frontend - Componentes

### Estructura de Componentes

```
src/
├── App.js                    # Componente principal
├── components/
│   ├── BusquedaCliente.jsx   # Formulario de búsqueda
│   ├── InformacionCliente.jsx # Visualización de cliente
│   ├── ReporteFidelizacion.jsx # Generación de reporte
│   └── Alerta.jsx            # Componente de alertas
└── services/
    └── api.js                # Servicios de API
```

### Componentes Principales

#### BusquedaCliente
- Formulario con tipo de documento y número de documento
- Carga dinámica de tipos de documento
- Validación de campos
- Manejo de estados de carga

#### InformacionCliente
- Muestra información completa del cliente
- Tabla de historial de compras
- Botones de exportación (CSV, Excel, TXT)
- Formateo de fechas y monedas

#### ReporteFidelizacion
- Botón para generar reporte de fidelización
- Descarga automática del archivo Excel

#### Alerta
- Muestra mensajes de error y éxito
- Auto-cierre después de 5 segundos
- Animaciones suaves

## Tecnologías Utilizadas

### Backend
- **Django 4.2.7**: Framework web de Python
- **Django REST Framework 3.14.0**: Framework para APIs REST
- **django-cors-headers 4.3.1**: Manejo de CORS
- **pandas 2.1.3**: Procesamiento de datos
- **openpyxl 3.1.2**: Generación de archivos Excel
- **SQLite**: Base de datos

### Frontend
- **React 18.2.0**: Biblioteca de UI
- **Axios 1.6.2**: Cliente HTTP
- **Tailwind CSS 3.3.6**: Framework de estilos
- **file-saver 2.0.5**: Descarga de archivos
- **xlsx 0.18.5**: Manipulación de Excel

## Flujos de Trabajo

### Búsqueda de Cliente

1. Usuario ingresa tipo y número de documento
2. Frontend envía petición GET a `/api/clientes/buscar/`
3. Backend consulta la base de datos
4. Si encuentra el cliente, retorna los datos
5. Frontend muestra la información del cliente

### Exportación de Datos

1. Usuario hace clic en botón de exportación (CSV/Excel/TXT)
2. Frontend envía petición GET a `/api/clientes/{id}/exportar/`
3. Backend genera el archivo en el formato solicitado
4. Backend retorna el archivo como respuesta
5. Frontend descarga el archivo automáticamente

### Reporte de Fidelización

1. Usuario hace clic en "Generar Reporte Excel"
2. Frontend envía petición GET a `/api/reporte-fidelizacion/generar/`
3. Backend consulta clientes con compras > $5'000.000 en último mes
4. Backend genera archivo Excel con pandas y openpyxl
5. Backend retorna el archivo Excel
6. Frontend descarga el archivo automáticamente

## Seguridad

### Consideraciones Implementadas

1. **Validación de datos**: Validación en modelos y serializadores
2. **CORS configurado**: Solo permite orígenes específicos
3. **Protección CSRF**: Activada en Django (aunque no se usa en API REST)
4. **Validación de email**: Validadores de email en modelo Cliente

### Recomendaciones para Producción

1. Implementar autenticación (JWT, OAuth2)
2. Usar HTTPS
3. Configurar rate limiting
4. Implementar logging y monitoreo
5. Validar y sanitizar todas las entradas
6. Usar variables de entorno para secretos
7. Implementar backup automático de base de datos

## Rendimiento

### Optimizaciones Implementadas

1. **Select Related**: Uso de `select_related` y `prefetch_related` en consultas
2. **Índices de base de datos**: Índices en campos frecuentemente consultados
3. **Paginación**: API REST con paginación por defecto
4. **Lazy Loading**: Componentes React cargados bajo demanda

### Recomendaciones

1. Implementar caché (Redis) para consultas frecuentes
2. Optimizar consultas con `only()` y `defer()`
3. Implementar compresión de respuestas
4. Usar CDN para archivos estáticos del frontend

## Testing

### Comandos de Prueba

```bash
# Backend
python manage.py test

# Frontend
npm test
```

### Datos de Prueba

El comando `seed_data` genera datos de prueba que incluyen:
- Al menos un cliente elegible para fidelización
- Varios clientes con diferentes tipos de documento
- Compras distribuidas en diferentes fechas

## Mantenimiento

### Logs

Los logs de Django se pueden configurar en `settings.py`:

```python
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

### Monitoreo

Recomendaciones:
- Implementar herramientas como Sentry para errores
- Usar herramientas de monitoreo de performance
- Configurar alertas para errores críticos

## Extensibilidad

### Agregar Nuevos Campos

1. Modificar el modelo en `clientes/models.py`
2. Crear migración: `python manage.py makemigrations`
3. Aplicar migración: `python manage.py migrate`
4. Actualizar serializadores en `clientes/serializers.py`
5. Actualizar componentes del frontend si es necesario

### Agregar Nuevos Endpoints

1. Agregar método en `clientes/views.py`
2. Agregar ruta en `clientes/urls.py`
3. Actualizar servicios en `frontend/src/services/api.js`
4. Crear o actualizar componentes del frontend

