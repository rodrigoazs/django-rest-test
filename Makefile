run:
	export DJANGO_DEVELOPMENT=True
	python3 manage.py runserver 0.0.0.0:8080

install:
	pip install pre-commit
	pip install -r requirements.txt
	pre-commit install
