#!/bin/bash

# Script para configurar ramas de despliegue en Vercel
# Este script ayuda a configurar el proyecto para desplegar desde múltiples ramas

echo "🚀 Configurando ramas de despliegue en Vercel..."
echo ""

# Verificar si Vercel CLI está instalado
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI no está instalado. Instalando..."
    npm install -g vercel
fi

echo "🔍 Verificando configuración actual del proyecto..."
echo ""

# Obtener información del proyecto
vercel project ls

echo ""
echo "📋 Para habilitar despliegues en ramas de desarrollo:"
echo ""
echo "1. Ve a tu dashboard de Vercel: https://vercel.com/dashboard"
echo "2. Selecciona tu proyecto: nada-records-techno-store"
echo "3. Ve a Settings > Git"
echo "4. En 'Production Branch', asegúrate de que esté configurado como 'main'"
echo "5. En 'Deploy Hooks', habilita 'Automatically deploy all pushed branches'"
echo "6. También puedes configurar 'Preview Deployments' para:"
echo "   - develop (para staging)"
echo "   - feature/* (para feature branches)"
echo ""
echo "📝 Configuración recomendada de ramas:"
echo "   - main: Producción"
echo "   - develop: Staging/Preview"
echo "   - feature/*: Preview para desarrollo"
echo ""

# Verificar ramas actuales
echo "🌳 Ramas actuales en el repositorio:"
git branch -a

echo ""
echo "✅ Para aplicar la configuración, ejecuta:"
echo "   vercel --prod (para desplegar main a producción)"
echo "   vercel (para desplegar rama actual como preview)"
echo ""
