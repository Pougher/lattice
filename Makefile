# creates a virtual environment

all:
	venv/bin/python3 lattice.py

virtual_env:
	mkdir -p cache
	python3 -m venv venv/
	venv/bin/python3 -m pip install matplotlib sympy pygame pillow

clean:
	rm cache/*
	rm -rf venv
