# Sistema de Consulta de Clientes - Rios del Desierto SAS

Sistema web desarrollado para el equipo de SAC (Servicio al Cliente) que permite consultar información de clientes mediante número de documento y generar reportes de fidelización.

## 🚀 Características

- ✅ Búsqueda de clientes por tipo y número de documento
- ✅ Visualización completa de información del cliente
- ✅ Exportación de datos en múltiples formatos (CSV, Excel, TXT)
- ✅ Reporte de fidelización de clientes (Excel)
- ✅ Interfaz moderna y responsive
- ✅ API REST completa

## 📋 Requisitos

- Python 3.8+
- Node.js 18+
- npm o yarn

## 🛠️ Instalación Rápida

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data --clientes 50
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm start
```

## 📚 Documentación

- [Guía de Implementación](Docs/GUIA_IMPLEMENTACION.md) - Instrucciones paso a paso para producción
- [Documentación Técnica](Docs/DOCUMENTACION_TECNICA.md) - Detalles técnicos del sistema
- [Requerimientos](Docs/requerimiento.md) - Especificaciones del proyecto

## 🏗️ Estructura del Proyecto

```
Cinte-Test/
├── backend/              # Aplicación Django
│   ├── config/           # Configuración de Django
│   ├── clientes/         # Aplicación de clientes
│   │   ├── models.py     # Modelos de datos
│   │   ├── views.py      # Vistas/API
│   │   ├── serializers.py # Serializadores
│   │   └── management/   # Comandos personalizados
│   └── manage.py
├── frontend/             # Aplicación React
│   ├── src/
│   │   ├── components/   # Componentes React
│   │   └── services/     # Servicios de API
│   └── public/
└── Docs/                 # Documentación
```

## 🔧 Tecnologías

### Backend
- Django 4.2.7
- Django REST Framework
- SQLite
- Pandas
- OpenPyXL

### Frontend
- React 18.2.0
- Tailwind CSS
- Axios
- File Saver

## 📝 Uso

1. **Buscar Cliente**: Ingrese el tipo y número de documento
2. **Ver Información**: Se muestra toda la información del cliente y sus compras
3. **Exportar**: Descargue la información en CSV, Excel o TXT
4. **Reporte Fidelización**: Genere reporte de clientes elegibles para fidelización

## 🧪 Datos de Prueba

El comando `seed_data` crea:
- 3 tipos de documento (NIT, Cédula, Pasaporte)
- 50 clientes (configurable)
- Compras asociadas
- Al menos un cliente elegible para fidelización

## 📦 Entregables

- ✅ Código fuente completo
- ✅ Base de datos implementada
- ✅ Guía de implementación
- ✅ Documentación técnica
- ✅ Scripts de instalación

## 👥 Desarrollo

Desarrollado siguiendo buenas prácticas:
- Arquitectura limpia y escalable
- Componentización del código
- ORM de Django
- API RESTful
- Interfaz responsive

## 📄 Licencia

Proyecto desarrollado para Rios del Desierto SAS.
