#!/usr/bin/env python3

"""
🚀 Elite Audit Dashboard - Real-time Performance Monitor
Live dashboard with DORA metrics and regional benchmarks
"""

import json
import os
import sys
from datetime import datetime
import subprocess

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print elite dashboard banner"""
    print("🚀" + "="*60 + "🚀")
    print("     ELITE AUDIT DASHBOARD - NADA RECORDS TECHNO STORE")
    print("🚀" + "="*60 + "🚀")
    print()

def load_metrics():
    """Load metrics from metrics.json"""
    try:
        with open('metrics.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ metrics.json not found. Run 'make metrics' first.")
        return None

def get_emoji_for_score(score):
    """Get emoji based on performance score"""
    if score >= 90:
        return "🚀"
    elif score >= 80:
        return "🏆"
    elif score >= 70:
        return "📈"
    elif score >= 60:
        return "📊"
    else:
        return "📉"

def get_dora_level_emoji(level):
    """Get emoji for DORA level"""
    if level == "Elite":
        return "🚀"
    elif level == "High":
        return "🏆"
    elif level == "Medium":
        return "📊"
    else:
        return "📉"

def calculate_dora_level(metric_type, value):
    """Calculate DORA level based on metric value"""
    if metric_type == "deployment_frequency":
        if value >= 7:
            return "Elite", "🚀"
        elif value >= 4:
            return "High", "🏆"
        elif value >= 1:
            return "Medium", "📊"
        else:
            return "Low", "📉"
    elif metric_type == "lead_time":
        if value <= 1:
            return "Elite", "🚀"
        elif value <= 4:
            return "High", "🏆"
        elif value <= 24:
            return "Medium", "📊"
        else:
            return "Low", "📉"
    elif metric_type == "change_failure_rate":
        if value <= 5:
            return "Elite", "🚀"
        elif value <= 15:
            return "High", "🏆"
        elif value <= 30:
            return "Medium", "📊"
        else:
            return "Low", "📉"
    
    return "Unknown", "❓"

def print_executive_summary(data):
    """Print executive summary dashboard"""
    overall = data['overall_performance']
    score = overall['score']
    emoji = get_emoji_for_score(score)
    
    print(f"🏆 PUNTUACIÓN GLOBAL: {score:.1f}/100 {emoji} {overall['assessment']}")
    print(f"🌍 RANKING MUNDIAL: {overall['global_ranking']}")
    print(f"⏰ ÚLTIMA ACTUALIZACIÓN: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def print_dora_metrics(data):
    """Print DORA metrics dashboard"""
    dora = data['dora_metrics']
    
    print("🎯 MÉTRICAS DORA:")
    print("─" * 50)
    
    # Deployment Frequency
    freq = dora['deployment_frequency_weekly']
    freq_level, freq_emoji = calculate_dora_level("deployment_frequency", freq)
    print(f"📦 Deployment Frequency: {freq:.1f}/semana {freq_emoji} {freq_level}")
    
    # Lead Time
    lead_time = dora['lead_time_hours']
    lead_level, lead_emoji = calculate_dora_level("lead_time", lead_time)
    print(f"⚡ Lead Time: {lead_time:.1f}h {lead_emoji} {lead_level}")
    
    # Change Failure Rate
    cfr = dora['change_failure_rate_percent']
    cfr_level, cfr_emoji = calculate_dora_level("change_failure_rate", cfr)
    print(f"🔧 Change Failure Rate: {cfr:.1f}% {cfr_emoji} {cfr_level}")
    
    print()

def print_regional_comparison(data):
    """Print regional comparison dashboard"""
    print("🌍 COMPARATIVA REGIONAL:")
    print("─" * 50)
    
    regions = {
        'SP': '🇪🇸 España',
        'EU': '🇪🇺 Europa',
        'US': '🇺🇸 USA'
    }
    
    for code, name in regions.items():
        if code in data['regional_comparisons']:
            comp = data['regional_comparisons'][code]
            score = comp['performance_vs_region']
            commits_delta = comp['commits_wk_delta']
            emoji = get_emoji_for_score(score)
            
            delta_sign = "+" if commits_delta >= 0 else ""
            print(f"{name}: {score:.0f}/100 {emoji} (commits Δ{delta_sign}{commits_delta:.1f})")
    
    print()

def print_project_vitals(data):
    """Print project vital statistics"""
    pm = data['project_metrics']
    
    print("📊 ESTADÍSTICAS DEL PROYECTO:")
    print("─" * 50)
    print(f"📈 Commits totales: {pm['commits_total']}")
    print(f"⏱️  Commits/semana: {pm['commits_per_week']:.1f}")
    print(f"👥 Contribuidores: {len(pm['authors_top'])}")
    print(f"⏰ Gap promedio: {pm['avg_gap_hours']:.1f}h")
    print(f"📅 Período analizado: {pm['window_days']} días")
    print(f"➕ Líneas añadidas: {pm['added_lines']:,}")
    print(f"➖ Líneas eliminadas: {pm['deleted_lines']:,}")
    print()

def print_scope_analysis(data):
    """Print monorepo scope analysis"""
    pm = data['project_metrics']
    scopes = pm['scope_counts']
    
    print("🎯 ANÁLISIS DE ALCANCE (MONOREPO):")
    print("─" * 50)
    
    total_commits = sum(scopes.values())
    for scope, count in sorted(scopes.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_commits) * 100
        if scope == "frontend":
            emoji = "🎨"
        elif scope == "backend":
            emoji = "⚙️"
        elif scope == "devops":
            emoji = "🚀"
        elif scope == "documentation":
            emoji = "📚"
        else:
            emoji = "🔀"
            
        print(f"{emoji} {scope.title()}: {count} commits ({percentage:.1f}%)")
    print()

def print_hotspots(data):
    """Print development hotspots"""
    pm = data['project_metrics']
    if 'hot_files' in pm:
        print("🔥 HOTSPOTS DE DESARROLLO:")
        print("─" * 50)
        
        for i, (file, changes) in enumerate(pm['hot_files'][:5], 1):
            print(f"{i}. {file} ({changes} cambios)")
        print()

def print_recommendations(data):
    """Print strategic recommendations"""
    overall = data['overall_performance']
    score = overall['score']
    
    print("💡 RECOMENDACIONES ESTRATÉGICAS:")
    print("─" * 50)
    
    if score < 90:
        dora = data['dora_metrics']
        
        if dora['deployment_frequency_weekly'] < 7:
            print("🚀 Aumentar frecuencia de deploys a >7/semana")
        
        if dora['lead_time_hours'] > 4:
            print("⚡ Reducir lead time a <4h con trunk-based development")
        
        if dora['change_failure_rate_percent'] > 15:
            print("🔧 Mejorar quality gates (<15% failure rate)")
        
        if score < 80:
            print("🧪 Incrementar cobertura de tests a >90%")
            print("📊 Implementar monitoring y observabilidad")
    
    print("🎯 Objetivo: Alcanzar nivel Elite (90+) - Top 10% mundial")
    print()

def print_elite_path(data):
    """Print path to elite level"""
    overall = data['overall_performance']
    score = overall['score']
    
    if score < 90:
        gap_to_elite = 90 - score
        print("🎯 CAMINO AL NIVEL ELITE:")
        print("─" * 50)
        print(f"📊 Puntos necesarios: +{gap_to_elite:.1f} para Elite (90+)")
        print("🏆 Nivel Elite = Top 10% mundial (Google, Netflix, Amazon)")
        print()
        
        print("Próximos hitos:")
        if score < 70:
            print("1️⃣ Alcanzar Good (70+) - Top 50%")
        elif score < 80:
            print("1️⃣ Alcanzar High (80+) - Top 25%")
        else:
            print("1️⃣ Alcanzar Elite (90+) - Top 10%")
        print()

def print_commands():
    """Print available commands"""
    print("🔧 COMANDOS DISPONIBLES:")
    print("─" * 50)
    print("make audit-all       # Auditoría completa")
    print("make metrics         # Regenerar métricas")
    print("make report          # Regenerar reporte")
    print("./elite_dashboard.py # Este dashboard")
    print()

def main():
    """Main dashboard function"""
    clear_screen()
    print_banner()
    
    # Load metrics
    data = load_metrics()
    if not data:
        sys.exit(1)
    
    # Print dashboard sections
    print_executive_summary(data)
    print_dora_metrics(data)
    print_regional_comparison(data)
    print_project_vitals(data)
    print_scope_analysis(data)
    print_hotspots(data)
    print_recommendations(data)
    print_elite_path(data)
    print_commands()
    
    print("🎉 Dashboard actualizado. Para datos en tiempo real, ejecuta 'make metrics' primero.")

if __name__ == "__main__":
    main()
