#!/usr/bin/env python3
"""
Enhanced Audit Report Generator with Regional Benchmarks and DORA Analysis
Generates professional-grade reports with international comparisons
"""

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

def parse_args():
    """Parse command line arguments."""
    ap = argparse.ArgumentParser(description='Generate enhanced audit report')
    ap.add_argument("--metrics", default="metrics.json", help="Path to enhanced metrics JSON")
    ap.add_argument("--coverage", default="coverage.xml", help="Path to coverage XML")
    ap.add_argument("--out", default="AUDIT_REPORT.md", help="Output Markdown file")
    return ap.parse_args()

def load_metrics(path):
    """Load metrics JSON file."""
    return json.load(open(path)) if Path(path).exists() else {}

def parse_coverage(path):
    """Parse coverage XML file."""
    if not Path(path).exists():
        return None
    try:
        return float(ET.parse(path).getroot().attrib.get("line-rate", 0.0)) * 100.0
    except:
        return None

def line(s):
    """Ensure string ends with newline."""
    return s if s.endswith("\n") else s + "\n"

def get_performance_emoji(score):
    """Get emoji based on performance score."""
    if score >= 90: return "🚀"
    elif score >= 80: return "🏆"
    elif score >= 70: return "📈"
    elif score >= 60: return "📊"
    else: return "📉"

def get_coverage_status(coverage):
    """Get coverage status with emoji."""
    if coverage is None:
        return "⚠️ No coverage data"
    elif coverage >= 90:
        return f"🚀 Elite ({coverage:.1f}%)"
    elif coverage >= 85:
        return f"🏆 Excellent ({coverage:.1f}%)"
    elif coverage >= 75:
        return f"📈 Good ({coverage:.1f}%)"
    elif coverage >= 60:
        return f"📊 Basic ({coverage:.1f}%)"
    else:
        return f"❌ Critical ({coverage:.1f}%)"

def main():
    """Main report generation function."""
    args = parse_args()
    
    print("📄 Generating enhanced audit report with benchmarks...")
    
    # Load data
    m = load_metrics(args.metrics)
    cov = parse_coverage(args.coverage)
    
    # Build report
    buf = []
    
    # Header with executive summary
    buf.append("# 🏆 Nada Records Techno Store — Informe de Auditoría Elite\n")
    buf.append(f"**Generado:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    buf.append(f"**Tech Stack:** Next.js + FastAPI + Azure + TypeScript\n\n")
    
    # Executive Dashboard
    buf.append("## 📊 Dashboard Ejecutivo\n\n")
    
    if m and "overall_performance" in m:
        overall = m["overall_performance"]
        buf.append(f"### Rendimiento Global: {get_performance_emoji(overall['score'])} {overall['assessment']}\n")
        buf.append(f"- **Puntuación Total:** {overall['score']}/100\n")
        buf.append(f"- **Ranking Global:** {overall.get('global_ranking', 'N/A')}\n")
    
    buf.append(f"- **Cobertura de Tests:** {get_coverage_status(cov)}\n")
    
    if m and "project_metrics" in m:
        pm = m["project_metrics"]
        buf.append(f"- **Actividad:** {pm['commits_total']} commits en {m['analysis_window']} días\n")
        buf.append(f"- **Cadencia:** {pm['commits_per_week']} commits/semana\n")
    
    buf.append("\n")
    
    # DORA Metrics Section
    if m and "dora_metrics" in m:
        dora = m["dora_metrics"]
        buf.append("## 🎯 Métricas DORA (DevOps Research & Assessment)\n\n")
        buf.append("| Métrica | Valor | Benchmark |\n")
        buf.append("|---------|-------|----------|\n")
        buf.append(f"| Frecuencia de Despliegue | {dora.get('deployment_frequency_weekly', 0):.1f}/semana | Elite: >7/sem |\n")
        buf.append(f"| Lead Time | {dora.get('lead_time_hours', 0):.1f}h | Elite: <24h |\n")
        buf.append(f"| Tasa de Fallo | {dora.get('change_failure_rate_percent', 0):.1f}% | Elite: <15% |\n")
        buf.append("\n")
    
    # Regional Comparisons
    if m and "regional_comparisons" in m:
        buf.append("## 🌍 Comparativa Regional (Δ vs Media)\n\n")
        buf.append("| Región | Score | Commits/sem | Lead Time | Deploy Freq | Nivel |\n")
        buf.append("|--------|-------|-------------|-----------|-------------|-------|\n")
        
        for region, comp in m["regional_comparisons"].items():
            score = comp["performance_vs_region"]
            emoji = get_performance_emoji(score)
            commits_delta = comp.get("commits_wk_delta", 0)
            lead_delta = comp.get("lead_time_delta_h", 0)
            deploy_delta = comp.get("deploy_freq_delta_wk", 0)
            
            buf.append(f"| {region} | {score}/100 {emoji} | ")
            buf.append(f"{'+' if commits_delta >= 0 else ''}{commits_delta:.1f} | ")
            buf.append(f"{'+' if lead_delta >= 0 else ''}{lead_delta:.1f}h | ")
            buf.append(f"{'+' if deploy_delta >= 0 else ''}{deploy_delta:.1f} | ")
            
            if score >= 90: level = "🚀 Elite"
            elif score >= 80: level = "🏆 Alto"
            elif score >= 70: level = "📈 Bueno"
            elif score >= 60: level = "📊 Medio"
            else: level = "📉 Bajo"
            
            buf.append(f"{level} |\n")
        
        buf.append("\n")
    
    # Detailed Metrics
    if m and "project_metrics" in m:
        pm = m["project_metrics"]
        buf.append("## 📈 Métricas Detalladas\n\n")
        buf.append(f"- **Ventana de Análisis:** {m['analysis_window']} días\n")
        buf.append(f"- **Commits Totales:** {pm['commits_total']} → {pm['commits_per_week']:.1f}/semana\n")
        
        if pm.get('avg_gap_hours'):
            buf.append(f"- **Gap Medio entre Commits:** {pm['avg_gap_hours']:.1f}h\n")
        
        buf.append(f"- **Impacto de Código:** +{pm.get('added_lines', 0):,} / -{pm.get('deleted_lines', 0):,} líneas\n")
        buf.append("\n")
        
        # Top Contributors
        if pm.get("authors_top"):
            buf.append("### 👥 Contribuidores Principales\n")
            for name, commits in pm["authors_top"][:5]:  # Top 5
                percentage = (commits / pm['commits_total']) * 100 if pm['commits_total'] > 0 else 0
                buf.append(f"- **{name}:** {commits} commits ({percentage:.1f}%)\n")
            buf.append("\n")
        
        # Scope Analysis (Monorepo)
        if pm.get("scope_counts"):
            buf.append("### 🎯 Áreas de Desarrollo (Monorepo)\n")
            for scope, count in pm["scope_counts"].items():
                percentage = (count / pm['commits_total']) * 100 if pm['commits_total'] > 0 else 0
                buf.append(f"- **{scope.title()}:** {count} commits ({percentage:.1f}%)\n")
            buf.append("\n")
        
        # Hotspots
        if pm.get("hot_files"):
            buf.append("### 🔥 Archivos Más Modificados\n")
            for path, changes in pm["hot_files"][:10]:  # Top 10
                buf.append(f"- `{path}` → {changes} cambios\n")
            buf.append("\n")
    
    # Coverage Analysis
    if cov is not None:
        buf.append("## 🧪 Análisis de Cobertura\n\n")
        buf.append(f"- **Cobertura Actual:** {cov:.2f}%\n")
        
        if cov >= 85:
            buf.append("- ✅ **PASSED:** Supera el umbral de calidad (85%)\n")
        else:
            gap = 85 - cov
            buf.append(f"- ❌ **FAILED:** Necesita {gap:.1f}% más para alcanzar el estándar\n")
        
        buf.append("\n")
    
    # Recommendations
    buf.append("## 💡 Recomendaciones Estratégicas\n\n")
    
    recommendations = []
    
    if m and "overall_performance" in m:
        score = m["overall_performance"]["score"]
        if score < 70:
            recommendations.append("🎯 **Crítico:** Mejorar cadencia de desarrollo y calidad")
        elif score < 85:
            recommendations.append("📈 **Importante:** Optimizar procesos para alcanzar nivel Elite")
    
    if cov is not None and cov < 85:
        recommendations.append("🧪 **Tests:** Incrementar cobertura para alcanzar estándar industrial")
    
    # DORA improvements
    if m and "dora_metrics" in m:
        dora = m["dora_metrics"]
        if dora.get("deployment_frequency_weekly", 0) < 7:
            recommendations.append("🚀 **Deploy:** Incrementar frecuencia de despliegue (objetivo: >7/semana)")
        if dora.get("lead_time_hours", 0) > 24:
            recommendations.append("⚡ **Lead Time:** Reducir tiempo de entrega (objetivo: <24h)")
        if dora.get("change_failure_rate_percent", 0) > 15:
            recommendations.append("🔧 **Calidad:** Reducir tasa de fallos (objetivo: <15%)")
    
    # General recommendations
    recommendations.extend([
        "🔐 **Seguridad:** Ejecutar `bandit` y `pip-audit` regularmente",
        "📦 **Dependencies:** Mantener dependencias actualizadas y sin vulnerabilidades",
        "🎨 **Code Style:** Usar `ruff` y `black` para consistencia de código",
        "📋 **Docs:** Mantener documentación técnica actualizada"
    ])
    
    for rec in recommendations:
        buf.append(f"- {rec}\n")
    
    buf.append("\n")
    
    # Footer
    buf.append("---\n\n")
    buf.append("**🚀 Nada Records Techno Store - Auditoría Elite**\n\n")
    buf.append(f"*Reporte generado automáticamente el {datetime.now().strftime('%Y-%m-%d')} con métricas DORA y benchmarks internacionales.*\n\n")
    buf.append("Para mejorar métricas: `make audit-all` • Para benchmarks: establecer variables `SP_COMMITS_WK`, `EU_COMMITS_WK`, `US_COMMITS_WK`\n")
    
    # Write report
    Path(args.out).write_text("".join(buf), encoding="utf-8")
    
    print(f"✅ Enhanced audit report generated: {args.out}")
    
    # Print executive summary
    if m and "overall_performance" in m:
        score = m["overall_performance"]["score"]
        assessment = m["overall_performance"]["assessment"]
        print(f"🏆 Overall Performance: {score}/100 ({assessment})")
    
    if cov is not None:
        print(f"🧪 Code Coverage: {cov:.1f}%")

if __name__ == "__main__":
    main()
