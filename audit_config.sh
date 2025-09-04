# 🚀 Elite Audit System - Independent Configuration
# This file ensures the audit system runs independently of main application workflows

# =============================================================================
# AUDIT SYSTEM ISOLATION CONFIGURATION
# =============================================================================

# 1. Independent Python Environment
AUDIT_PYTHON_ENV="audit_env"
AUDIT_REQUIREMENTS="audit_requirements.txt"

# 2. Isolated Execution Paths
AUDIT_SCRIPTS_DIR="scripts"
AUDIT_OUTPUT_DIR="audit_output"
AUDIT_TEMP_DIR=".audit_temp"

# 3. Non-Interfering File Patterns
AUDIT_FILES_PATTERN="audit_*|scripts/*|*_audit.*|ELITE_*|QUALITY_*|metrics.json|AUDIT_REPORT.md"

# 4. Safe Execution Commands (no CI/CD triggers)
AUDIT_COMMANDS=(
    "make metrics"
    "make report" 
    "make dashboard"
    "make benchmarks"
    "make audit-all"
    "./setup_elite_audit.sh"
    "./elite_dashboard.py"
)

# 5. Environment Variables for Isolation
export AUDIT_MODE="independent"
export SKIP_MAIN_WORKFLOWS="true"
export AUDIT_ONLY_MODE="true"

# 6. Git Ignore Patterns for Audit (don't commit temp files)
AUDIT_GITIGNORE_PATTERNS=(
    "audit_output/"
    ".audit_temp/"
    "*.audit.log"
    "audit_env/"
    "coverage.xml"
    "htmlcov/"
    ".pytest_cache/"
    "__pycache__/"
)

# =============================================================================
# SAFETY CHECKS
# =============================================================================

# Ensure audit system doesn't interfere with main application
check_audit_isolation() {
    echo "🔍 Checking audit system isolation..."
    
    # Check if running in audit mode
    if [[ "$AUDIT_ONLY_MODE" == "true" ]]; then
        echo "✅ Running in isolated audit mode"
        return 0
    fi
    
    # Warn if not isolated
    echo "⚠️  Warning: Not running in isolated mode"
    return 1
}

# Function to run audit safely
run_audit_safe() {
    export AUDIT_ONLY_MODE="true"
    export SKIP_MAIN_WORKFLOWS="true"
    "$@"
}

echo "🚀 Elite Audit System configured for independent operation"
echo "💡 Use 'source audit_config.sh && run_audit_safe make audit-all' for safe execution"
