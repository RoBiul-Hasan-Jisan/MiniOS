# MiniOS Python Simulation Makefile

.PHONY: all run test clean debug shell

all: run

run:
	@echo "Starting MiniOS Python Simulation..."
	@PYTHONPATH=src python main.py

test:
	@echo "Running tests..."
	@PYTHONPATH=src python -m pytest tests/ -v

clean:
	@echo "Cleaning up..."
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete
	@rm -rf logs/*.log
	@rm -f .coverage

debug:
	@echo "Starting MiniOS in debug mode..."
	@PYTHONPATH=src python -m pdb main.py

shell:
	@echo "Starting standalone shell..."
	@PYTHONPATH=src python -c "from src.apps.shell import Shell; from src.kernel.kernel import Kernel; s = Shell(Kernel()); s.run()"

calculator:
	@echo "Starting calculator..."
	@PYTHONPATH=src python -c "from src.apps.calculator import Calculator; c = Calculator(); c.run()"

coverage:
	@echo "Running tests with coverage..."
	@PYTHONPATH=src coverage run -m pytest tests/
	@coverage report -m

profile:
	@echo "Profiling system..."
	@PYTHONPATH=src python -m cProfile -o minios.prof main.py
	@echo "Profile data saved to minios.prof"

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  run        - Start MiniOS simulation"
	@echo "  test       - Run test suite"
	@echo "  clean      - Clean generated files"
	@echo "  debug      - Start with debugger"
	@echo "  shell      - Run standalone shell"
	@echo "  calculator - Run calculator app"
	@echo "  coverage   - Run tests with coverage"
	@echo "  profile    - Profile system performance"