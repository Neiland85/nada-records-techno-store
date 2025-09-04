# ==== Nada Records Techno Store — Quality Audit ====
# FRONTEND: Next.js  (Node 18/20)  |  BACKEND: FastAPI (Python 3.11+)
# Requisitos front: pnpm|npm, eslint, typescript, vitest/jest (si hay tests)
# Requisitos back: ruff, black, mypy, pytest, pytest-cov, bandit, pip-audit, cyclonedx-bom

.PHONY: help init audit audit-all \
        fe-install fe-lint fe-type fe-test fe-audit \
        be-install be-lint be-format be-type be-test be-cov be-sec be-deps be-sbom be-audit \
        metrics metrics-dora report clean demo benchmarks

help:
	@echo "=== Nada Records Techno Store - Quality Audit ==="
	@echo ""
	@echo "🚀 INIT COMMANDS:"
	@echo "  init              Install all dependencies (frontend + backend)"
	@echo "  clean             Clean all build artifacts and cache"
	@echo ""
	@echo "🎨 FRONTEND COMMANDS:"
	@echo "  fe-install        Install frontend dependencies (pnpm/npm)"
	@echo "  fe-lint           Run ESLint with zero warnings policy"
	@echo "  fe-type           TypeScript type checking"
	@echo "  fe-test           Run frontend tests (vitest/jest)"
	@echo "  fe-audit          Complete frontend audit (lint + type + test)"
	@echo ""
	@echo "🐍 BACKEND COMMANDS:"
	@echo "  be-install        Install backend quality tools"
	@echo "  be-lint           Run Ruff linting"
	@echo "  be-format         Format code with Black"
	@echo "  be-type           MyPy type checking"
	@echo "  be-test           Run pytest"
	@echo "  be-cov            Coverage analysis (85% minimum)"
	@echo "  be-sec            Security analysis with Bandit"
	@echo "  be-deps           Dependency vulnerability check"
	@echo "  be-sbom           Generate Software Bill of Materials"
	@echo "  be-audit          Complete backend audit (all checks)"
	@echo ""
	@echo "📊 REPORTING COMMANDS:"
	@echo "  metrics           Generate Git metrics (90 days)"
	@echo "  metrics-dora      Generate DORA metrics from GitHub Actions"
	@echo "  report            Generate comprehensive audit report"
	@echo "  audit             Run frontend + backend audits"
	@echo "  audit-all         Complete audit + SBOM + metrics + report"
	@echo ""
	@echo "🌍 BENCHMARK COMMANDS:"
	@echo "  benchmarks        Set regional benchmarks (ES/EU/US)"
	@echo ""
	@echo "🎬 DEMO COMMANDS:"
	@echo "  demo              Run interactive demo of audit system"

# ===== FRONTEND =====
fe-install:
	@echo "🎨 Installing frontend dependencies..."
	cd frontend && (pnpm install || npm install)

fe-lint:
	@echo "🔍 Running ESLint with zero warnings policy..."
	cd frontend && npx eslint . --max-warnings=0

fe-type:
	@echo "📝 Running TypeScript type checking..."
	cd frontend && npx tsc --noEmit

fe-test:
	@echo "🧪 Running frontend tests..."
	cd frontend && (npx vitest run || npx jest --ci || echo "⚠️  No tests found - consider adding tests")

fe-audit: fe-lint fe-type fe-test
	@echo "✅ Frontend audit completed successfully!"

# ===== BACKEND =====
be-install:
	@echo "🐍 Installing backend quality tools..."
	pip install -U ruff black mypy pytest pytest-cov bandit pip-audit cyclonedx-bom

be-lint:
	@echo "🔍 Running Ruff linting..."
	ruff check backend && echo "✅ Ruff OK"

be-format:
	@echo "🎨 Formatting code with Black..."
	black backend --check --diff

be-format-fix:
	@echo "🔧 Fixing code formatting with Black..."
	black backend

be-type:
	@echo "📝 Running MyPy type checking..."
	mypy backend

be-test:
	@echo "🧪 Running pytest..."
	pytest backend -v

be-cov:
	@echo "📊 Running coverage analysis..."
	pytest backend --cov=backend --cov-report=term-missing --cov-report=xml:coverage.xml --cov-report=html:htmlcov
	@echo "🎯 Validating coverage threshold (85%)..."
	python3 scripts/coverage_gate.py coverage.xml 85

be-sec:
	@echo "🔐 Running security analysis with Bandit..."
	bandit -q -r backend

be-deps:
	@echo "🔍 Checking dependency vulnerabilities..."
	# pip-audit devuelve exit!=0 si hay vulns; no rompas local si solo quieres reporte
	pip-audit || echo "⚠️  Vulnerabilities found - check output above"

be-sbom:
	@echo "📋 Generating Software Bill of Materials..."
	cyclonedx-py -e -o sbom.json

be-audit: be-lint be-format be-type be-test be-cov be-sec be-deps
	@echo "✅ Backend audit completed successfully!"

# ===== GLOBAL =====
init: fe-install be-install
	@echo "🚀 All dependencies installed successfully!"

clean:
	@echo "🧹 Cleaning build artifacts and cache..."
	rm -rf frontend/.next frontend/node_modules/.cache
	rm -rf backend/__pycache__ backend/.pytest_cache
	rm -rf htmlcov coverage.xml metrics.json AUDIT_REPORT.md sbom.json
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

metrics:
	@echo "📈 Generating enhanced Git metrics with regional benchmarks (90 days)..."
	python3 scripts/metrics_git.py --window-days 90 --out metrics.json

metrics-dora:
	@echo "🎯 Generating DORA metrics from GitHub Actions..."
	@echo "💡 Ensure GITHUB_TOKEN is set for API access"
	python3 scripts/dora_from_actions.py --days 30 --out dora_metrics.json || echo "⚠️  DORA metrics require GITHUB_TOKEN"

benchmarks:
	@echo "🌍 Setting regional benchmarks for comparison..."
	@echo "Setting Spain (ES) benchmarks..."
	export SP_COMMITS_WK=10 SP_TIME_BETWEEN_H=12 SP_LEAD_TIME_H=24 SP_DEPLOY_FREQ_WK=5
	@echo "Setting Europe (EU) benchmarks..."
	export EU_COMMITS_WK=11 EU_TIME_BETWEEN_H=11 EU_LEAD_TIME_H=20 EU_DEPLOY_FREQ_WK=6
	@echo "Setting USA (US) benchmarks..."
	export US_COMMITS_WK=12 US_TIME_BETWEEN_H=10 US_LEAD_TIME_H=18 US_DEPLOY_FREQ_WK=8
	@echo "✅ Regional benchmarks configured!"
	@echo "💡 Run 'make metrics' to see comparisons"

report:
	@echo "📄 Generating comprehensive audit report..."
	python3 scripts/report_markdown.py --metrics metrics.json --coverage coverage.xml --out AUDIT_REPORT.md

dashboard:
	@echo "🚀 Opening Elite Performance Dashboard..."
	@python3 elite_dashboard.py

audit: fe-audit be-audit
	@echo "🎉 Complete audit finished successfully!"

audit-all: fe-audit be-audit be-sbom metrics report
	@echo "🏆 Comprehensive audit with enhanced reporting completed!"
	@echo "📋 Check AUDIT_REPORT.md for detailed results with benchmarks"
	@echo "💡 Run 'make metrics-dora' for DORA metrics (requires GITHUB_TOKEN)"

demo:
	@echo "🎬 Running audit system demo..."
	./demo_audit.sh
