#!/bin/bash

# 🚀 Setup Elite Audit System - INDEPENDENT MODE
# This script operates WITHOUT affecting main application code or workflows

echo "🏆 === SISTEMA DE AUDITORÍA ELITE (MODO INDEPENDIENTE) ==="
echo ""
echo "🔒 MODO SEGURO ACTIVADO: No afecta código principal ni workflows"
echo ""

# Activate safe mode
export AUDIT_ONLY_MODE=true
export SKIP_MAIN_WORKFLOWS=true

# Set regional benchmarks (independent analysis)
echo "🌍 Configurando benchmarks regionales (modo independiente)..."

export SP_COMMITS_WK=10
export SP_TIME_BETWEEN_H=12
export SP_LEAD_TIME_H=24
export SP_DEPLOY_FREQ_WK=5

export EU_COMMITS_WK=11
export EU_TIME_BETWEEN_H=11
export EU_LEAD_TIME_H=20
export EU_DEPLOY_FREQ_WK=6

export US_COMMITS_WK=12
export US_TIME_BETWEEN_H=10
export US_LEAD_TIME_H=18
export US_DEPLOY_FREQ_WK=8

echo "✅ Benchmarks configurados (modo seguro):"
echo "   🇪🇸 España: $SP_COMMITS_WK commits/sem"
echo "   🇪🇺 Europa:  $EU_COMMITS_WK commits/sem"
echo "   🇺🇸 USA:     $US_COMMITS_WK commits/sem"

echo ""
echo "📊 === ANÁLISIS INDEPENDIENTE ==="

# Use independent makefile for safe operation
echo "🔍 Generando métricas (modo independiente)..."
make -f audit.mk metrics

echo ""
echo "📄 Generando reporte (modo seguro)..."
make -f audit.mk report

echo ""
echo "📈 === RESULTADOS (INDEPENDIENTES) ==="

if [ -f "metrics.json" ]; then
    echo "✅ Métricas generadas exitosamente (modo seguro)"
    
    python3 -c "
import json
try:
    with open('metrics.json', 'r') as f:
        data = json.load(f)
        
        pm = data['project_metrics']
        dora = data['dora_metrics']
        overall = data['overall_performance']
        
        print(f'📊 RESUMEN EJECUTIVO (INDEPENDIENTE):')
        print(f'   • Puntuación: {overall[\"score\"]}/100 ({overall[\"assessment\"]})')
        print(f'   • Ranking: {overall[\"global_ranking\"]}')
        print(f'   • Commits/semana: {pm[\"commits_per_week\"]}')
        print()
        print(f'🎯 MÉTRICAS DORA (SEGURAS):')
        print(f'   • Deploy Freq: {dora[\"deployment_frequency_weekly\"]:.1f}/semana')
        print(f'   • Lead Time: {dora[\"lead_time_hours\"]:.1f}h')
        print(f'   • Failure Rate: {dora[\"change_failure_rate_percent\"]:.1f}%')
except Exception as e:
    print('⚠️  Error en modo seguro')
"
else
    echo "❌ Error generando métricas (verificar permisos)"
fi

echo ""
echo "🔧 === COMANDOS SEGUROS DISPONIBLES ==="
echo ""
echo "make -f audit.mk all        # Auditoría completa independiente"
echo "make -f audit.mk dashboard  # Dashboard seguro"
echo "make -f audit.mk benchmarks # Benchmarks regionales"
echo ""
echo "🎉 === SISTEMA ELITE INDEPENDIENTE LISTO ==="
echo ""
echo "🔒 Operación completamente aislada del código principal!"
echo "📊 Reporte: AUDIT_REPORT.md"
echo "🚀 Dashboard: make -f audit.mk dashboard"
