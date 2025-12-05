# Guía de Implementación - Sistema de Consulta de Clientes

Esta guía describe paso a paso cómo implementar el sistema en un ambiente productivo.

## Requisitos Previos

### Backend (Python/Django)
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- virtualenv (opcional pero recomendado)

### Frontend (React)
- Node.js 18.x o superior
- npm o yarn

## Paso 1: Configuración del Backend

### 1.1. Clonar o copiar el repositorio

```bash
git clone <url-del-repositorio>
cd Cinte-Test
```

### 1.2. Crear y activar entorno virtual (Recomendado)

```bash
# En Linux/Mac
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 1.3. Instalar dependencias

```bash
cd backend
pip install -r requirements.txt
```

### 1.4. Configurar base de datos

```bash
# Crear las migraciones
python manage.py makemigrations

# Aplicar las migraciones
python manage.py migrate
```

### 1.5. Crear superusuario (Opcional, para acceso al admin)

```bash
python manage.py createsuperuser
```

### 1.6. Poblar base de datos con datos de prueba

```bash
python manage.py seed_data --clientes 50
```

Este comando creará:
- 3 tipos de documento (NIT, Cédula, Pasaporte)
- 50 clientes (o el número especificado)
- Compras asociadas a cada cliente
- Al menos un cliente elegible para fidelización

### 1.7. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## Paso 2: Configuración del Frontend

### 2.1. Instalar dependencias

```bash
cd frontend
npm install
```

### 2.2. Configurar variables de entorno

Crear un archivo `.env` en la carpeta `frontend`:

```env
REACT_APP_API_URL=http://localhost:8000/api
```

Para producción, cambiar la URL por la del servidor backend.

### 2.3. Ejecutar en modo desarrollo

```bash
npm start
```

La aplicación estará disponible en `http://localhost:3000`

### 2.4. Compilar para producción

```bash
npm run build
```

Esto generará una carpeta `build` con los archivos optimizados para producción.

## Paso 3: Despliegue en Producción

### 3.1. Backend en Producción

#### Opción A: Usando Gunicorn y Nginx

1. Instalar Gunicorn:
```bash
pip install gunicorn
```

2. Configurar Gunicorn:
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

3. Configurar Nginx como proxy reverso (ejemplo de configuración):

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /ruta/a/tu/proyecto/backend/staticfiles/;
    }
}
```

#### Opción B: Usando Docker

Crear un `Dockerfile` para el backend:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### 3.2. Frontend en Producción

#### Opción A: Servir archivos estáticos con Nginx

1. Compilar la aplicación:
```bash
npm run build
```

2. Configurar Nginx para servir los archivos estáticos:

```nginx
server {
    listen 80;
    server_name dominio.com;
    root /ruta/frontend/build;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Opción B: Usando Docker

Crear un `Dockerfile` para el frontend:

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 3.3. Configuraciones de Seguridad para Producción

1. **Cambiar SECRET_KEY en settings.py**:
   - Generar una nueva clave secreta
   - Usar variables de entorno para almacenarla

2. **Configurar DEBUG = False**:
   - En `backend/config/settings.py`, cambiar `DEBUG = False`

3. **Configurar ALLOWED_HOSTS**:
   - Agregar el dominio de producción a `ALLOWED_HOSTS`

4. **Configurar CORS**:
   - Actualizar `CORS_ALLOWED_ORIGINS` con los dominios permitidos

5. **Usar HTTPS**:
   - Configurar certificado SSL
   - Redirigir HTTP a HTTPS

## Paso 4: Verificación

1. Verificar que el backend responda correctamente:
   - `http://tu-servidor:8000/api/tipos-documento/`

2. Verificar que el frontend se conecte al backend

3. Probar la búsqueda de clientes

4. Probar la exportación de datos

5. Probar la generación del reporte de fidelización

## Solución de Problemas Comunes

### Error: "ModuleNotFoundError"
- Verificar que todas las dependencias estén instaladas
- Verificar que el entorno virtual esté activado

### Error: "No module named 'django'"
- Ejecutar `pip install -r requirements.txt`

### Error de CORS en el navegador
- Verificar que `CORS_ALLOWED_ORIGINS` incluya la URL del frontend
- Verificar que el middleware de CORS esté configurado

### Error: "Cliente no encontrado"
- Verificar que la base de datos tenga datos
- Ejecutar `python manage.py seed_data`

## Mantenimiento

### Backup de Base de Datos

```bash
# Backup
cp backend/db.sqlite3 backup/db.sqlite3.$(date +%Y%m%d_%H%M%S)

# Restaurar
cp backup/db.sqlite3.backup backend/db.sqlite3
```

### Actualizar Dependencias

```bash
# Backend
pip install --upgrade -r requirements.txt

# Frontend
npm update
```

## Contacto y Soporte

Para soporte técnico, contactar al equipo de desarrollo.

