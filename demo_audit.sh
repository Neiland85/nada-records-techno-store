#!/bin/bash

# 🏆 Demo del Sistema de Auditoría de Calidad - Nada Records Techno Store
# Este script demuestra todas las capacidades del sistema de auditoría

echo "🎉 === DEMO: Sistema de Auditoría de Calidad ==="
echo ""

# Limpiar estado anterior
echo "🧹 Limpiando estado anterior..."
make clean > /dev/null 2>&1

echo ""
echo "📋 === 1. INFORMACIÓN DEL SISTEMA ==="
make help

echo ""
echo "📦 === 2. INSTALACIÓN DE DEPENDENCIAS ==="
echo "🎨 Instalando dependencias del frontend..."
make fe-install

echo ""
echo "🐍 Instalando herramientas de calidad del backend..."
make be-install

echo ""
echo "🔍 === 3. ANÁLISIS DE CALIDAD ==="
echo ""

echo "📝 Frontend: Linting con ESLint..."
make fe-lint || echo "❌ ESLint encontró problemas - normal en desarrollo"

echo ""
echo "📝 Frontend: Verificación de tipos TypeScript..."
make fe-type || echo "❌ TypeScript encontró errores - normal en desarrollo"

echo ""
echo "🧪 Frontend: Ejecutando tests..."
make fe-test || echo "❌ Tests fallaron - normal sin configuración completa"

echo ""
echo "🔍 Backend: Linting con Ruff..."
make be-lint

echo ""
echo "🎨 Backend: Verificación de formato con Black..."
make be-format || echo "❌ Formato necesita corrección"

echo ""
echo "📝 Backend: Verificación de tipos con MyPy..."
make be-type || echo "❌ MyPy encontró problemas - normal sin configuración completa"

echo ""
echo "🧪 Backend: Ejecutando tests..."
make be-test || echo "❌ Tests fallaron - normal sin configuración completa"

echo ""
echo "📊 === 4. GENERACIÓN DE MÉTRICAS ==="
echo ""

echo "📈 Generando métricas Git (90 días)..."
make metrics

echo ""
echo "📄 Generando reporte de auditoría..."
make report

echo ""
echo "🎯 === 5. RESULTADOS ==="
echo ""

if [ -f "metrics.json" ]; then
    echo "✅ metrics.json generado exitosamente"
    echo "📊 Resumen de métricas:"
    python3 -c "
import json
with open('metrics.json', 'r') as f:
    data = json.load(f)
    stats = data['commit_stats']
    velocity = data['velocity']
    print(f'   • Commits: {stats[\"commit_count\"]}')
    print(f'   • Contribuidores: {stats[\"contributor_count\"]}')
    print(f'   • Líneas añadidas: {stats[\"lines_added\"]:,}')
    print(f'   • Velocidad: {velocity[\"commits_per_day\"]:.2f} commits/día')
"
else
    echo "❌ No se pudo generar metrics.json"
fi

echo ""

if [ -f "AUDIT_REPORT.md" ]; then
    echo "✅ AUDIT_REPORT.md generado exitosamente"
    echo "📄 Reporte de $(wc -l < AUDIT_REPORT.md) líneas creado"
else
    echo "❌ No se pudo generar AUDIT_REPORT.md"
fi

echo ""
echo "🗂️ === 6. ARCHIVOS GENERADOS ==="
ls -la *.json *.md | grep -E "\.(json|md)$" || echo "No hay archivos de reporte"

echo ""
echo "💡 === 7. PRÓXIMOS PASOS ==="
echo ""
echo "Para usar el sistema de auditoría:"
echo "• make audit          - Auditoría rápida"
echo "• make audit-all      - Auditoría completa + reportes"
echo "• make be-cov         - Análisis de cobertura (cuando tengas tests)"
echo "• make be-sec         - Análisis de seguridad"
echo "• make clean          - Limpiar archivos temporales"
echo ""
echo "📖 Consulta QUALITY_AUDIT_README.md para documentación completa"

echo ""
echo "🏆 === DEMO COMPLETADO ==="
echo "El sistema de auditoría está listo para uso en desarrollo profesional!"
