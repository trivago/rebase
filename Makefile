env:
	pipenv --venv || pipenv --python 3.6

activate:
	pipenv shell

setup:
	pipenv install -e . --skip-lock --ignore-pipfile -v

test:
	pipenv run python setup.py test
