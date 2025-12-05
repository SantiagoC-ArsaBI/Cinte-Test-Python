#!/bin/bash

# Script de inicio rápido para desarrollo

echo "🚀 Iniciando Sistema de Consulta de Clientes"
echo ""

# Verificar si el entorno virtual existe
if [ ! -d "backend/venv" ]; then
    echo "📦 Creando entorno virtual..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# Activar entorno virtual y verificar dependencias del backend
echo "🔧 Configurando backend..."
cd backend
source venv/bin/activate 2>/dev/null || venv\Scripts\activate 2>/dev/null

if [ ! -f "db.sqlite3" ]; then
    echo "📊 Creando base de datos..."
    python manage.py migrate
    echo "🌱 Poblando base de datos con datos de prueba..."
    python manage.py seed_data --clientes 50
fi

echo "✅ Backend listo"
echo ""

# Verificar dependencias del frontend
echo "🔧 Configurando frontend..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias del frontend..."
    npm install
fi

echo "✅ Frontend listo"
echo ""
echo "📝 Para iniciar el sistema:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend"
echo "  npm start"
echo ""
echo "🌐 Backend: http://localhost:8000"
echo "🌐 Frontend: http://localhost:3000"
echo ""

