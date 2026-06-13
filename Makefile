EASY1 = maps/easy/01_linear_path.txt
EASY2 = maps/easy/02_simple_fork.txt
EASY3 = maps/easy/03_basic_capacity.txt
MED1 = maps/medium/01_dead_end_trap.txt
MED2 = maps/medium/02_circular_loop.txt
MED3 = maps/medium/03_priority_puzzle.txt
HARD1 = maps/hard/01_maze_nightmare.txt
HARD2 = maps/hard/02_capacity_hell.txt
HARD3 = maps/hard/03_ultimate_challenge.txt
CHAL = maps/challenger/01_the_impossible_dream.txt

UV = uv run

.PHONY: install run debug clean lint lint-strict

run:
	$(UV) python3 src/main.py --file_path=$(MED2)

install:
	uv sync
	touch $$(find .venv -name "webcolors" -type d)/py.typed

debug:
	$(UV) python3 -m pdb src/main.py

clean:
	rm -rf src/__pycache__
	rm -rf .mypy_cache

lint:
	$(UV) flake8 src
	$(UV) mypy src \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	$(UV) flake8 src
	$(UV) mypy --strict src 