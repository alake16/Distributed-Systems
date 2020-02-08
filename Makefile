freeze:
	pip3 freeze | grep -v "pkg-resources" > requirements.txt

test:
	python3 -m unittest discover -s app/tests

lint:
    pylint app

init:
    mkdir app/quizzes
    mkdir app/quizzes/taken
    mkdir app/quizzes/untaken

