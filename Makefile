yaml:
	yamllint -d '{"extends": "default", "ignore": ".venv"}' -s .

check-django:
	python manage.py check --fail-level WARNING
	DJANGO_ENV=production python manage.py check --deploy --fail-level WARNING

style:
	flake8 .
	yamllint -d '{"extends": "default", "ignore": ".venv" }' -s .

pytest:
	pytest --dead-fixtures && pytest --junitxml=report.xml --cov=server \
	--cov=tests --cov-branch --cov-report=term-missing:skip-covered \
	--cov-fail-under=100 --cov-report xml:coverage.xml

ci-yaml:
	yamllint -d '{"extends": "default", "ignore": ".venv" }' -s .

ci-migrations:
	python manage.py lintmigrations \
	--exclude-apps axes sites filer easy_thumbnails actstream
	--warnings-as-errors

ci-mypy:
	mypy manage.py server $(find tests -name '*.py')

flake8:
	flake8 .

pytest-coverage:
	pytest --cov=server/apps --cov-branch --cov-report html

celery:
	docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
	celery -A server worker -l info --concurrency=4
