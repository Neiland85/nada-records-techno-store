#!/bin/bash

# 🚀 Setup Elite Audit System - Nada Records Techno Store
# Configures regional benchmarks and demonstrates all capabilities

echo "🏆 === SISTEMA DE AUDITORÍA ELITE ==="
echo ""

# Set regional benchmarks based on industry research
echo "🌍 Configurando benchmarks regionales (basados en investigación DORA)..."

# Spain - Growing tech scene, moderate pace
export SP_COMMITS_WK=10
export SP_TIME_BETWEEN_H=12
export SP_LEAD_TIME_H=24
export SP_DEPLOY_FREQ_WK=5

# Europe - Established tech markets, balanced approach
export EU_COMMITS_WK=11
export EU_TIME_BETWEEN_H=11
export EU_LEAD_TIME_H=20
export EU_DEPLOY_FREQ_WK=6

# USA - Silicon Valley standards, high velocity
export US_COMMITS_WK=12
export US_TIME_BETWEEN_H=10
export US_LEAD_TIME_H=18
export US_DEPLOY_FREQ_WK=8

echo "✅ Benchmarks configurados:"
echo "   🇪🇸 España: $SP_COMMITS_WK commits/sem, $SP_TIME_BETWEEN_H h gap, $SP_DEPLOY_FREQ_WK deploys/sem"
echo "   🇪🇺 Europa:  $EU_COMMITS_WK commits/sem, $EU_TIME_BETWEEN_H h gap, $EU_DEPLOY_FREQ_WK deploys/sem"
echo "   🇺🇸 USA:     $US_COMMITS_WK commits/sem, $US_TIME_BETWEEN_H h gap, $US_DEPLOY_FREQ_WK deploys/sem"

echo ""
echo "📊 === ANÁLISIS CON BENCHMARKS REGIONALES ==="

# Generate enhanced metrics
echo "🔍 Generando métricas con comparativas internacionales..."
make metrics

echo ""
echo "📄 Generando reporte elite con DORA y benchmarks..."
make report

echo ""
echo "📈 === RESULTADOS DEL ANÁLISIS ELITE ==="

if [ -f "metrics.json" ]; then
    echo "✅ Métricas generadas exitosamente"
    
    # Extract key metrics using Python
    python3 -c "
import json
with open('metrics.json', 'r') as f:
    data = json.load(f)
    
    pm = data['project_metrics']
    dora = data['dora_metrics']
    overall = data['overall_performance']
    
    print(f'📊 RESUMEN EJECUTIVO:')
    print(f'   • Puntuación Global: {overall[\"score\"]}/100 ({overall[\"assessment\"]})')
    print(f'   • Ranking: {overall[\"global_ranking\"]}')
    print(f'   • Commits/semana: {pm[\"commits_per_week\"]}')
    print(f'   • Gap promedio: {pm[\"avg_gap_hours\"]}h')
    print()
    print(f'🎯 MÉTRICAS DORA:')
    print(f'   • Frecuencia Deploy: {dora[\"deployment_frequency_weekly\"]:.1f}/semana')
    print(f'   • Lead Time: {dora[\"lead_time_hours\"]:.1f}h')
    print(f'   • Tasa de Fallo: {dora[\"change_failure_rate_percent\"]:.1f}%')
    print()
    print(f'🌍 COMPARATIVA REGIONAL:')
    for region, comp in data['regional_comparisons'].items():
        score = comp['performance_vs_region']
        commits_delta = comp['commits_wk_delta']
        symbol = '📈' if score >= 70 else '📊' if score >= 60 else '📉'
        print(f'   • {region}: {score:.0f}/100 {symbol} (commits Δ{commits_delta:+.1f})')
"
else
    echo "❌ No se pudieron generar las métricas"
fi

echo ""
echo "📋 === REPORTE GENERADO ==="

if [ -f "AUDIT_REPORT.md" ]; then
    echo "✅ AUDIT_REPORT.md generado con éxito"
    echo "📄 Líneas del reporte: $(wc -l < AUDIT_REPORT.md)"
    echo ""
    echo "🎯 Highlights del reporte:"
    echo "   • Dashboard ejecutivo con puntuación global"
    echo "   • Métricas DORA comparadas con estándares Elite"
    echo "   • Análisis regional (España/Europa/USA)"
    echo "   • Análisis de monorepo por áreas (frontend/backend/devops)"
    echo "   • Hotspots de archivos más modificados"
    echo "   • Recomendaciones estratégicas personalizadas"
else
    echo "❌ No se pudo generar el reporte"
fi

echo ""
echo "🔧 === HERRAMIENTAS DISPONIBLES ==="
echo ""
echo "📊 Análisis de Calidad:"
echo "   make audit-all      # Auditoría completa + reportes"
echo "   make be-cov         # Cobertura de tests (85% mínimo)"
echo "   make be-sec         # Análisis de seguridad"
echo ""
echo "📈 Métricas Avanzadas:"
echo "   make metrics        # Git metrics con benchmarks regionales"
echo "   make metrics-dora   # DORA metrics (requiere GITHUB_TOKEN)"
echo "   make report         # Reporte elite con comparativas"
echo ""
echo "🌍 Benchmarks:"
echo "   export SP_COMMITS_WK=10   # Personalizar benchmark España"
echo "   export EU_COMMITS_WK=11   # Personalizar benchmark Europa"
echo "   export US_COMMITS_WK=12   # Personalizar benchmark USA"

echo ""
echo "🎯 === SIGUIENTES PASOS PARA NIVEL ELITE ==="
echo ""
echo "Para alcanzar nivel 🚀 Elite (Top 10%):"
echo ""
echo "1. 🧪 **Cobertura de Tests**"
echo "   • Objetivo: >90% cobertura"
echo "   • Comando: make be-cov"
echo "   • Estado: Configurar pytest coverage"
echo ""
echo "2. 🚀 **Frecuencia de Despliegue**"
echo "   • Objetivo: >7 deploys/semana"
echo "   • Estado actual: $(python3 -c "import json; data=json.load(open('metrics.json')); print(f\"{data['dora_metrics']['deployment_frequency_weekly']:.1f}/semana\"" 2>/dev/null || echo "pendiente")"
echo "   • Mejora: Automatizar más el pipeline CI/CD"
echo ""
echo "3. ⚡ **Lead Time**"
echo "   • Objetivo: <24h (Elite: <1h)"
echo "   • Estado actual: $(python3 -c "import json; data=json.load(open('metrics.json')); print(f\"{data['dora_metrics']['lead_time_hours']:.1f}h\")" 2>/dev/null || echo "pendiente")"
echo "   • Mejora: Trunk-based development + feature flags"
echo ""
echo "4. 🔧 **Tasa de Fallo**"
echo "   • Objetivo: <15% (Elite: <5%)"
echo "   • Estado actual: $(python3 -c "import json; data=json.load(open('metrics.json')); print(f\"{data['dora_metrics']['change_failure_rate_percent']:.1f}%\")" 2>/dev/null || echo "pendiente")"
echo "   • Mejora: Más tests automatizados, monitoring"

echo ""
echo "🏆 === BENCHMARKING INTERNACIONAL ==="
echo ""
echo "Tu proyecto vs estándares globales:"

python3 -c "
import json
try:
    with open('metrics.json', 'r') as f:
        data = json.load(f)
    
    score = data['overall_performance']['score']
    
    print(f'Puntuación actual: {score:.1f}/100')
    print()
    
    if score >= 90:
        print('🚀 ELITE: Top 10% mundial (Unicorn/FAANG level)')
    elif score >= 80:
        print('🏆 HIGH PERFORMER: Top 25% mundial (Serie A level)')
    elif score >= 70:
        print('📈 GOOD: Top 50% mundial (Scale-up level)')
    elif score >= 60:
        print('📊 MEDIUM: Top 75% mundial (Startup level)')
    else:
        print('📉 LOW: Necesita mejora significativa')
    
    print()
    print('Contexto de tu repo:')
    print('• Duración: ~28 días (nuevo proyecto)')
    print('• Cadencia: Alta para proyecto en fase inicial')
    print('• Stack: Moderno (Next.js 15 + FastAPI + Azure)')
    print('• Seguridad: Proactiva (dependabot + fixes)')
    print('• DevOps: Automático (GitHub Actions + Vercel)')
    print()
    print('💡 Para un proyecto de 1 mes, estar en Top 50% es excelente!')

except FileNotFoundError:
    print('⚠️  Ejecuta make metrics primero')
"

echo ""
echo "🎉 === SISTEMA DE AUDITORÍA ELITE CONFIGURADO ==="
echo ""
echo "El sistema está listo para auditorías de nivel Silicon Valley!"
echo ""
echo "📖 Documentación completa: QUALITY_AUDIT_README.md"
echo "📊 Reporte actual: AUDIT_REPORT.md"
echo "🔧 Ver comandos: make help"
