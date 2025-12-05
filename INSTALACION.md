# Guía Rápida de Instalación

## Requisitos Previos

- Python 3.8 o superior
- Node.js 18.x o superior
- npm o yarn

## Instalación del Backend

```bash
# 1. Navegar a la carpeta backend
cd backend

# 2. Crear entorno virtual (si no existe)
python3 -m venv venv

# 3. Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Crear migraciones
python manage.py makemigrations

# 6. Aplicar migraciones
python manage.py migrate

# 7. Poblar base de datos con datos de prueba
python manage.py seed_data --clientes 50

# 8. (Opcional) Crear superusuario para admin
python manage.py createsuperuser

# 9. Ejecutar servidor
python manage.py runserver
```

El backend estará disponible en: `http://localhost:8000`

## Instalación del Frontend

```bash
# 1. Navegar a la carpeta frontend
cd frontend

# 2. Instalar dependencias
npm install

# 3. Configurar variables de entorno
# Crear archivo .env con:
# REACT_APP_API_URL=http://localhost:8000/api

# 4. Ejecutar en modo desarrollo
npm start
```

El frontend estará disponible en: `http://localhost:3000`

## Verificación

1. Abrir navegador en `http://localhost:3000`
2. Probar búsqueda de cliente
3. Verificar exportación de datos
4. Probar generación de reporte de fidelización

## Solución de Problemas

### Error: "python3-venv no disponible"
```bash
sudo apt install python3.12-venv
```

### Error: "ModuleNotFoundError"
```bash
# Asegurarse de que el entorno virtual esté activado
source venv/bin/activate
pip install -r requirements.txt
```

### Error de CORS
Verificar que en `backend/config/settings.py` esté configurado:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

