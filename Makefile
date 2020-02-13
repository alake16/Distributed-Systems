SHELL  := /bin/bash
freeze:
	pip3 freeze | grep -v "pkg-resources" > requirements.txt

test:
	python3 -m unittest discover -s app/tests

init:
	python3 -m venv venv
	source venv/bin/activate
	pip3 install -r requirements.txt
