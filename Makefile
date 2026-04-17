VENV = .venv
BIN = ${VENV}/bin
PY = $(BIN)/python3
PIP = $(BIN)/pip
RM = rm -rf

REQUIREMENT	= flake8 mypy poetry

C_RESET		= \033[0m
C_GREEN		= \033[032m
C_BLUE		= \033[034m
C_MAGENTA	= \033[035m


${VENV}:
	@if [ ! -d ${VENV} ]; then \
		echo "$(C_BLUE)Creating virtual environment...$(C_RESET)"; \
		python3 -m venv ${VENV}; \
		$(PIP) install --upgrade pip; \
		$(PIP) install lib/mlx-2.2-py3-none-any.whl; \
		$(PIP) install ${REQUIREMENT}; \
		echo "${C_MAGENTA}Project dependencies installed${C_RESET}"; \
	fi


run: ${VENV}
	@${PY} a_maze_ing.py config.txt

install: ${VENV}

debug: ${VENV}
	@${PY} -m pdb a_maze_ing.py config.txt

clean:
	@echo "${C_BLUE}Removing temporary files or caches\n...${C_RESET}"
	@${RM} .mypy_cache
	@${RM} */__pycache__
	@${RM} */*/__pycache__
	@echo "${C_GREEN}Our project environment is clean${C_RESET}"

lint: ${VENV}
	@echo "${C_BLUE}Running flake8\n...${C_RESET}"
	@${PY} -m flake8 . --exclude=${VENV}
	@echo "${C_BLUE}Running mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs\n...${C_BLUE}"
	
	@${PY} -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	@echo "${C_BLUE}Everything is safe${C_RESET}"

lint-strict: ${VENV}
	@echo "${C_BLUE}Running flake8\n...${C_RESET}"
	@${PY} -m flake8 . --exclude=${VENV}
	@echo "${C_GREEN}flake8 done successfully\n\n${C_RESET}"
	@echo "${C_BLUE}Running mypy --strict${C_RESET}"
	@echo "${C_MAGENTA}Note: 'mlx' is a third-party library without type hints; related mypy warnings are expected.${C_RESET}"
	@echo "${C_BLUE}...${C_RESET}"
	@${PY} -m mypy . --strict

.PHONY: install run clean lint lint-strict
