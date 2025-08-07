#!/bin/bash

# Script para configurar despliegues automáticos en Vercel para múltiples ramas
# Ejecutar: ./scripts/configure-vercel-deployment.sh

set -e

echo "🚀 Configurando despliegues automáticos en Vercel..."
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Verificar si estamos en un repositorio git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: No estás en un repositorio Git.${NC}"
    exit 1
fi

# Verificar si Vercel CLI está instalado
if ! command -v vercel &> /dev/null; then
    echo -e "${YELLOW}📦 Vercel CLI no está instalado. Instalando...${NC}"
    npm install -g vercel
fi

echo -e "${BLUE}🔍 Verificando configuración actual...${NC}"
echo ""

# Login a Vercel si no está autenticado
if ! vercel whoami > /dev/null 2>&1; then
    echo -e "${YELLOW}🔐 Iniciando sesión en Vercel...${NC}"
    vercel login
fi

# Verificar proyecto actual
echo -e "${BLUE}📋 Información del proyecto:${NC}"
echo ""

# Listar ramas disponibles
echo -e "${BLUE}🌳 Ramas disponibles:${NC}"
git branch -a | grep -E "(main|develop|feature/)"

echo ""
echo -e "${GREEN}✅ Configuración recomendada para despliegues:${NC}"
echo ""
echo -e "${YELLOW}Production Branch (main):${NC}"
echo "  - Despliegues automáticos desde 'main'"
echo "  - URL: https://nada-records-techno-store.vercel.app"
echo ""
echo -e "${YELLOW}Preview Branches:${NC}"
echo "  - develop: https://nada-records-techno-store-git-develop.vercel.app"
echo "  - feature/*: https://nada-records-techno-store-git-feature-*.vercel.app"
echo ""

# Instrucciones para configurar manualmente
echo -e "${BLUE}📝 Para completar la configuración:${NC}"
echo ""
echo "1. Ve a tu dashboard de Vercel:"
echo "   https://vercel.com/dashboard"
echo ""
echo "2. Selecciona tu proyecto y ve a Settings > Git"
echo ""
echo "3. Configura las siguientes opciones:"
echo "   ✓ Production Branch: main"
echo "   ✓ Deploy all branches: ENABLED"
echo "   ✓ Deploy only production branch: DISABLED"
echo ""
echo "4. En Settings > Environment Variables, configura:"
echo "   - NEXT_PUBLIC_API_URL para cada ambiente"
echo "   - Variables específicas por rama según .env.vercel.example"
echo ""

# Verificar si el proyecto ya está vinculado
if [ -f ".vercel/project.json" ]; then
    echo -e "${GREEN}✅ Proyecto ya vinculado a Vercel${NC}"
    
    # Mostrar configuración actual
    echo ""
    echo -e "${BLUE}🔧 Configuración actual del proyecto:${NC}"
    cat .vercel/project.json | jq '.'
else
    echo -e "${YELLOW}⚠️  Proyecto no vinculado a Vercel${NC}"
    echo ""
    read -p "¿Quieres vincular este proyecto ahora? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        vercel link
    fi
fi

echo ""
echo -e "${GREEN}🎉 Configuración completada!${NC}"
echo ""
echo -e "${BLUE}🚀 Para desplegar:${NC}"
echo "  - Rama main: push automático → producción"
echo "  - Rama develop: push automático → preview"
echo "  - Feature branches: push automático → preview"
echo ""
echo -e "${BLUE}📱 URLs de despliegue:${NC}"
echo "  - Producción: https://nada-records-techno-store.vercel.app"
echo "  - Preview: https://nada-records-techno-store-git-[branch].vercel.app"
echo ""
