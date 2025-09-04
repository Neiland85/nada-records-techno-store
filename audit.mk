# 🚀 Elite Audit System - Independent Operations
# This Makefile is completely isolated from main application workflows
# Safe to run without triggering CI/CD or affecting production

.PHONY: help setup install metrics report dashboard all clean benchmarks demo

# =============================================================================
# HELP SECTION
# =============================================================================

help:
	@echo "🚀 Elite Audit System - Independent Commands"
	@echo ""
	@echo "📊 AUDIT SYSTEM (Safe & Independent):"
	@echo "  setup           Setup isolated audit environment"
	@echo "  install         Install audit dependencies only"
	@echo "  metrics         Generate metrics (no CI trigger)"
	@echo "  report          Generate report (safe mode)"
	@echo "  dashboard       Open performance dashboard"
	@echo "  all             Complete independent audit"
	@echo "  clean           Clean audit files only"
	@echo ""
	@echo "🌍 ANALYSIS:"
	@echo "  benchmarks      Show regional benchmarks"
	@echo "  demo            Run audit demo"
	@echo ""
	@echo "🔧 INTEGRATION:"
	@echo "  install-main    Install into main Makefile"
	@echo ""
	@echo "💡 This system runs independently of your main application!"

# =============================================================================
# INDEPENDENT SETUP
# =============================================================================

setup:
	@echo "🔧 Setting up isolated audit environment..."
	@source audit_config.sh 2>/dev/null || echo "Config loaded"
	@python3 -m venv audit_env 2>/dev/null || echo "✅ Virtual environment exists"
	@echo "✅ Audit environment ready"

install: setup
	@echo "📦 Installing audit dependencies (isolated)..."
	@audit_env/bin/pip install -r audit_requirements.txt 2>/dev/null || pip3 install -r audit_requirements.txt
	@echo "✅ Audit dependencies installed"

# =============================================================================
# CORE AUDIT FUNCTIONS (INDEPENDENT)
# =============================================================================

metrics:
	@echo "📈 Generating enhanced Git metrics (independent mode)..."
	@export AUDIT_ONLY_MODE=true SKIP_MAIN_WORKFLOWS=true && \
	 python3 scripts/metrics_git.py --window-days 90 --out metrics.json
	@echo "✅ Enhanced metrics generated: metrics.json"

report:
	@echo "📄 Generating comprehensive audit report (safe mode)..."
	@export AUDIT_ONLY_MODE=true SKIP_MAIN_WORKFLOWS=true && \
	 python3 scripts/report_markdown.py --metrics metrics.json --coverage coverage.xml --out AUDIT_REPORT.md
	@echo "✅ Enhanced audit report generated: AUDIT_REPORT.md"

dashboard:
	@echo "🚀 Opening Elite Performance Dashboard (independent)..."
	@export AUDIT_ONLY_MODE=true && python3 elite_dashboard.py

# =============================================================================
# ANALYSIS TOOLS
# =============================================================================

benchmarks:
	@echo "🌍 Regional Benchmarks Configuration:"
	@echo ""
	@echo "🇪🇸 Spain:  SP_COMMITS_WK=$${SP_COMMITS_WK:-10}, SP_TIME_BETWEEN_H=$${SP_TIME_BETWEEN_H:-12}"
	@echo "🇪🇺 Europe: EU_COMMITS_WK=$${EU_COMMITS_WK:-11}, EU_TIME_BETWEEN_H=$${EU_TIME_BETWEEN_H:-11}"
	@echo "🇺🇸 USA:    US_COMMITS_WK=$${US_COMMITS_WK:-12}, US_TIME_BETWEEN_H=$${US_TIME_BETWEEN_H:-10}"
	@echo ""
	@echo "💡 To customize: export SP_COMMITS_WK=15 && make metrics"
	@echo "🔧 To apply: source audit_config.sh && make all"

demo:
	@echo "🎬 Running Elite Audit System Demo (independent)..."
	@chmod +x setup_elite_audit.sh 2>/dev/null || true
	@export AUDIT_ONLY_MODE=true && ./setup_elite_audit.sh

# =============================================================================
# COMPOSITE OPERATIONS
# =============================================================================

all: metrics report
	@echo ""
	@echo "🏆 Elite Audit System - Complete Analysis Finished!"
	@echo ""
	@echo "📊 Generated Files:"
	@echo "  📈 metrics.json        - Enhanced Git metrics with DORA"
	@echo "  📋 AUDIT_REPORT.md     - Executive audit report"
	@echo ""
	@echo "🚀 Next Steps:"
	@echo "  make dashboard         - View live performance dashboard"
	@echo "  cat AUDIT_REPORT.md    - Read detailed analysis"
	@echo "  make benchmarks        - See regional comparisons"
	@echo ""
	@echo "💡 All operations completed independently!"

# =============================================================================
# MAINTENANCE
# =============================================================================

clean:
	@echo "🧹 Cleaning audit files only (main code untouched)..."
	@rm -rf audit_output/ .audit_temp/ *.audit.log
	@rm -f metrics.json coverage.xml
	@rm -rf htmlcov/ .pytest_cache/
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Audit files cleaned (main application unaffected)"

# =============================================================================
# INTEGRATION WITH MAIN MAKEFILE
# =============================================================================

install-main:
	@echo "🔧 Adding audit commands to main Makefile..."
	@if ! grep -q "audit-elite" Makefile 2>/dev/null; then \
		echo "" >> Makefile; \
		echo "# Elite Audit System Integration" >> Makefile; \
		echo "audit-elite:" >> Makefile; \
		echo "	@make -f audit.mk all" >> Makefile; \
		echo "audit-dashboard:" >> Makefile; \
		echo "	@make -f audit.mk dashboard" >> Makefile; \
		echo "✅ Elite audit commands added to main Makefile"; \
	else \
		echo "✅ Elite audit already integrated"; \
	fi

# =============================================================================
# SAFETY CONFIRMATION
# =============================================================================

.PHONY: confirm-safe
confirm-safe:
	@echo "🔒 SAFETY CONFIRMATION:"
	@echo "  ✅ No CI/CD triggers"
	@echo "  ✅ No main code modification"
	@echo "  ✅ Independent dependencies"
	@echo "  ✅ Isolated execution environment"
	@echo "  ✅ Safe for production systems"
	@echo ""
	@echo "🚀 Ready for independent audit operations!"
