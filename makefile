run:
	python3 evaluate.py -s $(s) -c $(c)

experiments:
	$(MAKE) run s=500 c=0.75
	$(MAKE) run s=500 c=0.85
	$(MAKE) run s=500 c=0.90
	$(MAKE) run s=1000 c=0.75
	$(MAKE) run s=1000 c=0.85
	$(MAKE) run s=1000 c=0.90

help:
	@echo "Available commands:"
	@echo "  make run s=500 c=0.75         It runs the script with the specified parameters"