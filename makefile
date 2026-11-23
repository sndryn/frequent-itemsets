# Default parameters (override with: make run s=500 c=0.9)
s ?= 1000
c ?= 0.75

# Support thresholds and confidence thresholds used by `make experiments`
S_VALUES = 500 600 700 800 900 1000 1500 2000
C_VALUES = 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95

.PHONY: run experiments help

run:
	python3 evaluate.py -s $(s) -c $(c)

# For each s the frequent itemsets are mined once and rules are generated
# for every c. Results are appended to results.csv.
experiments:
	rm -f results.csv
	for sv in $(S_VALUES); do \
		python3 evaluate.py -s $$sv -c $(C_VALUES) --csv results.csv || exit 1; \
	done

help:
	@echo "Available commands:"
	@echo "  make run                  runs with s=1000, c=0.75 (defaults)"
	@echo "  make run s=500 c=0.9      runs with the specified parameters"
	@echo "  make experiments          runs all s and c values of the report (writes results.csv)"
