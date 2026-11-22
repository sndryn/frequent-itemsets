run:
	python3 evaluate.py -s $(s) -c $(c)

help:
	@echo "Available commands:"
	@echo "  make run s=500 c=0.75         It runs the script with the specified parameters"