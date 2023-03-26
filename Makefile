SHELL=/bin/bash
.DEFAULT_GOAL := help
PROJECT_SLUG=new-game-server

reset: ## Reset your local environment. Useful after switching branches, etc.
reset: poetry-install reset-db django-migrate django-user-passwords django-dev-createsuperuser

check: ## Check for any obvious errors in the project's setup.
check: pipdeptree-check django-check

format: ## Run this project's code formatters.
format: black-format isort-format

lint: ## Lint the project.
lint: black-lint isort-lint

poetry-install:
	poetry install

run-server:
	poetry run ./manage.py runserver

makemigrations:
	poetry run ./manage.py makemigrations

# Pip
pip-install-local: venv-check
	pip install -r requirements/local.txt

# Django
django-check: django-check-missing-migrations django-check-validate-templates

django-test: django-collectstatic
	PYTHONWARNINGS=all coverage run --include="apps/*" --omit=*/migrations/* ./manage.py test --noinput . apps
	PYTHONWARNINGS=all coverage report -m --fail-under 97

django-check-missing-migrations:
	./manage.py makemigrations --check --dry-run

django-collectstatic:
	./manage.py collectstatic --verbosity 0 --noinput

django-check-validate-templates:
	./manage.py validate_templates --verbosity 0

django-dev-createsuperuser: DJANGO_DEV_USERNAME ?= admin@admin.co.uk
django-dev-createsuperuser: DJANGO_DEV_PASSWORD ?= password
django-dev-createsuperuser: DJANGO_DEV_EMAIL ?= admin@admin.co.uk
django-dev-createsuperuser:
	@echo "import sys; from django.contrib.auth import get_user_model; obj = get_user_model().objects.create_superuser('$(DJANGO_DEV_USERNAME)', '$(DJANGO_DEV_EMAIL)', '$(DJANGO_DEV_PASSWORD)');" | python manage.py shell >> /dev/null
	@echo
	@echo "Superuser details: "
	@echo
	@echo "    $(DJANGO_DEV_USERNAME):$(DJANGO_DEV_PASSWORD)"
	@echo

django-user-passwords: DJANGO_USER_PASSWORD ?= password
django-user-passwords:
	@echo "from django.contrib.auth.hashers import make_password; from django.contrib.auth import get_user_model; get_user_model().objects.update(password=make_password('$(DJANGO_USER_PASSWORD)'));" | python manage.py shell >> /dev/null

django-migrate:
	poetry run ./manage.py migrate

# DB
reset-db: drop-db create-db

drop-db:
	dropdb --if-exists gardenserver_django

create-db:
	createdb gardenserver_django

# Black
black-lint:
	black --line-length 120 --exclude '/migrations/' --check apps project

black-format:
	black --line-length 120 --exclude '/migrations/' apps project

#pipdeptree
pipdeptree-check:
	pipdeptree --warn fail > /dev/null

# ISort
isort-lint:
	isort --check-only --diff apps project -l 120

isort-format:
	isort apps project -l 120

# Flake8
flake8-lint:
	flake8 apps project