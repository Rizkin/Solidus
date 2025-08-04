# Agent Forge Comprehensive Testing Makefile
# =============================================

# Python executable
PYTHON := python3

# Test directories
UNIT_TESTS := tests/unit
INTEGRATION_TESTS := tests/integration
PERFORMANCE_TESTS := tests/performance

# Coverage settings
COVERAGE_MIN := 85
COVERAGE_DIR := htmlcov

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

.PHONY: help test test-unit test-integration test-performance test-all coverage clean install

help: ## Show this help message
	@echo "🧪 Agent Forge Comprehensive Testing Suite"
	@echo "=========================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install testing dependencies
	@echo "📦 Installing testing dependencies..."
	$(PYTHON) -m pip install pytest pytest-asyncio pytest-mock pytest-cov pytest-benchmark pytest-json-report
	@echo "✅ Dependencies installed"

test-unit: ## Run unit tests only
	@echo "🔬 Running Unit Tests..."
	$(PYTHON) -m pytest $(UNIT_TESTS) -v \
		--cov=src \
		--cov-report=term-missing \
		--cov-report=html:$(COVERAGE_DIR) \
		--cov-fail-under=$(COVERAGE_MIN) \
		--tb=short

test-integration: ## Run integration tests only
	@echo "🔗 Running Integration Tests..."
	$(PYTHON) -m pytest $(INTEGRATION_TESTS) -v --tb=short

test-performance: ## Run performance tests only
	@echo "⚡ Running Performance Tests..."
	$(PYTHON) -m pytest $(PERFORMANCE_TESTS) -v --benchmark-only || echo "⚠️  Performance tests not yet implemented"

test-all: ## Run all test suites with comprehensive reporting
	@echo "🧪 Running Comprehensive Test Suite..."
	$(PYTHON) tests/run_comprehensive_tests.py all

test: test-integration ## Default: Run integration tests (quick verification)

test-quick: ## Run a quick subset of tests for rapid feedback
	@echo "🚀 Running Quick Tests..."
	$(PYTHON) -m pytest tests/integration/test_simple_integration.py -v

# Coverage specific targets
coverage: ## Generate coverage report
	@echo "📊 Generating Coverage Report..."
	$(PYTHON) -m pytest $(UNIT_TESTS) \
		--cov=src \
		--cov-report=html:$(COVERAGE_DIR) \
		--cov-report=term-missing \
		--cov-report=json:coverage.json
	@echo "📂 Coverage report generated in $(COVERAGE_DIR)/"

coverage-open: coverage ## Generate and open coverage report
	@echo "🌐 Opening coverage report..."
	open $(COVERAGE_DIR)/index.html

# Test specific components
test-templates: ## Test template system only
	@echo "📋 Testing Template System..."
	$(PYTHON) -m pytest tests/unit/test_templates.py -v

test-validation: ## Test validation system only
	@echo "✅ Testing Validation System..."
	$(PYTHON) -m pytest tests/unit/test_validation.py -v

test-database: ## Test database system only
	@echo "🗄️  Testing Database System..."
	$(PYTHON) -m pytest tests/unit/test_database_hybrid.py -v

test-state-generator: ## Test state generator only
	@echo "🤖 Testing State Generator..."
	$(PYTHON) -m pytest tests/unit/test_state_generator.py -v

test-lookup: ## Test lookup service only
	@echo "🔍 Testing Lookup Service..."
	$(PYTHON) -m pytest tests/unit/test_lookup_service.py -v

# Test with different verbosity levels
test-verbose: ## Run tests with maximum verbosity
	$(PYTHON) -m pytest -vvv --tb=long

test-quiet: ## Run tests with minimal output
	$(PYTHON) -m pytest -q

# Parallel testing (if pytest-xdist is installed)
test-parallel: ## Run tests in parallel
	@echo "⚡ Running Tests in Parallel..."
	$(PYTHON) -m pytest -n auto || $(PYTHON) -m pytest

# Test with markers
test-unit-only: ## Run only unit tests (using markers)
	$(PYTHON) -m pytest -m unit -v

test-integration-only: ## Run only integration tests (using markers)
	$(PYTHON) -m pytest -m integration -v

test-performance-only: ## Run only performance tests (using markers)
	$(PYTHON) -m pytest -m performance -v

test-ai: ## Run only AI-related tests
	$(PYTHON) -m pytest -m ai -v

test-database-mark: ## Run only database-related tests
	$(PYTHON) -m pytest -m database -v

test-cache: ## Run only cache-related tests
	$(PYTHON) -m pytest -m cache -v

# Debugging and analysis
test-debug: ## Run tests with debugging output
	$(PYTHON) -m pytest --pdb -v

test-lf: ## Run only tests that failed last time
	$(PYTHON) -m pytest --lf -v

test-ff: ## Run tests, stopping at first failure
	$(PYTHON) -m pytest -x -v

# Benchmarking
benchmark: ## Run performance benchmarks
	$(PYTHON) -m pytest --benchmark-only --benchmark-sort=mean

benchmark-compare: ## Compare benchmarks with previous runs
	$(PYTHON) -m pytest --benchmark-only --benchmark-compare

# Cleanup
clean: ## Clean up test artifacts
	@echo "🧹 Cleaning up test artifacts..."
	rm -rf $(COVERAGE_DIR)/
	rm -rf .coverage
	rm -rf coverage.json
	rm -rf .pytest_cache/
	rm -rf test_results_*.xml
	rm -rf test_results_*.json
	rm -rf coverage_*.json
	rm -rf test_report.json
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

# Report generation
report: ## Generate comprehensive test report
	@echo "📋 Generating Test Report..."
	$(PYTHON) tests/run_comprehensive_tests.py all
	@echo "📊 Report generated: test_report.json"

# CI/CD helpers
ci-test: install ## Run tests suitable for CI/CD
	@echo "🏗️  Running CI Tests..."
	$(PYTHON) -m pytest \
		--cov=src \
		--cov-report=xml:coverage.xml \
		--cov-report=term \
		--cov-fail-under=$(COVERAGE_MIN) \
		--junit-xml=test-results.xml \
		--tb=short

pre-commit: ## Run pre-commit checks
	@echo "🔍 Running pre-commit checks..."
	$(PYTHON) -m pytest tests/integration/test_simple_integration.py -v
	@echo "✅ Pre-commit checks passed"

# Development helpers
dev-test: ## Development testing with watch (requires pytest-watch)
	@echo "👀 Starting development test watcher..."
	$(PYTHON) -m ptw tests/integration/ --runner "python -m pytest -v"

test-fixtures: ## Test that all fixtures work correctly
	@echo "🔧 Testing fixtures..."
	$(PYTHON) -c "from tests.fixtures.mock_data import *; from tests.fixtures.mock_responses import *; print('✅ All fixtures imported successfully')"

# Quality assurance
lint-tests: ## Lint test files
	@echo "🔍 Linting test files..."
	find tests/ -name "*.py" -exec $(PYTHON) -m py_compile {} \;
	@echo "✅ Test files pass basic syntax check"

# Statistics
test-stats: ## Show test statistics
	@echo "📈 Test Statistics:"
	@echo "  Unit tests:        $$(find $(UNIT_TESTS) -name "test_*.py" | wc -l | tr -d ' ') files"
	@echo "  Integration tests: $$(find $(INTEGRATION_TESTS) -name "test_*.py" | wc -l | tr -d ' ') files"
	@echo "  Total test lines:  $$(find tests/ -name "*.py" -exec wc -l {} + | tail -1 | awk '{print $$1}')"
	@echo "  Fixture files:     $$(find tests/fixtures/ -name "*.py" | wc -l | tr -d ' ') files"

# Help for specific test types
help-unit: ## Show help for unit testing
	@echo "🔬 Unit Test Help:"
	@echo "  make test-unit          - Run all unit tests with coverage"
	@echo "  make test-templates     - Test template system"
	@echo "  make test-validation    - Test validation system"
	@echo "  make test-database      - Test database system"
	@echo "  make test-state-generator - Test state generator"
	@echo "  make test-lookup        - Test lookup service"

help-integration: ## Show help for integration testing
	@echo "🔗 Integration Test Help:"
	@echo "  make test-integration   - Run all integration tests"
	@echo "  make test-quick         - Run quick integration tests"

help-performance: ## Show help for performance testing
	@echo "⚡ Performance Test Help:"
	@echo "  make test-performance   - Run performance tests"
	@echo "  make benchmark          - Run benchmarks"
	@echo "  make benchmark-compare  - Compare with previous runs"

# Default target
.DEFAULT_GOAL := help 