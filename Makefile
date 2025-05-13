.PHONY: clean install install-dev lint format test coverage build docs

# Default target
all: install-dev lint test

# Setup virtual environment and install dependencies
install:
	pip install -e .

# Install development dependencies
install-dev:
	pip install -r requirements/requirements-dev.txt
	pip install -e .
	pre-commit install

# Run linter
lint:
	black --check --line-length=120 src tests
	mypy src

# Format code
format:
	black --line-length=120 src tests

# Run tests
test:
	pytest tests/

# Run tests with coverage
coverage:
	pytest tests/ --cov=svg_generator --cov-report=html
	@echo "Coverage report generated in htmlcov/"

# Build package
build:
	python -m build
	@echo "Build completed in dist/"

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .coverage htmlcov/
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete

# Generate documentation
docs:
	@echo "Documentation generation not configured yet. Add Sphinx or MkDocs configuration."
