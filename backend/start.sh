#!/bin/bash

# Script para iniciar el backend de Nada Records Techno Store
echo "🚀 Iniciando Nada Records Techno Store Backend..."

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py no encontrado. Ejecuta desde el directorio backend."
    exit 1
fi

# Verificar configuración
echo "✅ Verificando configuración..."
python -c "from app.core.config import settings; print('✅ Configuración OK')" || exit 1

# Verificar servicio de email
echo "✅ Verificando servicio de email..."
python -c "from app.core.email import EmailService; print('✅ EmailService OK')" || exit 1

# Iniciar el servidor
echo "🌟 Iniciando servidor en http://localhost:8000"
echo "📧 SendGrid configurado y listo"
echo "🎵 API para tienda de música techno"
echo ""
echo "Endpoints disponibles:"
echo "  • http://localhost:8000/ - Página principal"
echo "  • http://localhost:8000/health - Health check"
echo "  • http://localhost:8000/docs - Documentación Swagger"
echo "  • http://localhost:8000/api/v1/test-email - Test de configuración email"
echo ""

# Ejecutar uvicorn
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
