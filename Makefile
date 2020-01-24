freeze:
	pip3 freeze | grep -v "pkg-resources" > requirements.txt

test:
	python3 app/tests.py

lint:
	pylint app
