.ONESHELL:
PYTHON=python3
PIP=pip3
PROJECT=drb

ifeq (, $(shell which $(PYTHON)))
 $(error "No $(PYTHON) in $(PATH), consider doing apt-get install python3.6+")
endif

all: lint test coverage docs dist
.PHONY: all

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || $(PYTHON) -m venv venv
	. venv/bin/activate
	$(PIP) install wheel
	$(PYTHON) -m pip install -Ur requirements.txt --no-cache-dir
	$(PYTHON) -m pip install -Ur requirements-dev.txt --no-cache-dir
	$(PYTHON) -m pip install -Ur requirements-doc.txt --no-cache-dir
	touch venv/bin/activate

test: venv
	. venv/bin/activate
	$(PYTHON) -m unittest discover
	$(PYTHON) -m unittest -v

clean:
	@rm -rf htmlcov
	@find -iname "*.pyc" -delete
	@find -name "__pycache__" -delete
	@rm -f .coverage coverage.xml
	@rm -rf .htmlcov
	@rm -rf .pytest_cache
	@rm -rf cache
	@rm -rf public

coverage: venv
	. venv/bin/activate
	coverage run --include '$(PROJECT)/*'  --omit $(PROJECT)/_version.py  -m unittest -v
	coverage xml
	coverage html

docs: venv
	. venv/bin/activate
	sphinx-build -b html docs public

lint: venv
	. venv/bin/activate
	pycodestyle --show-source --show-pep8 --exclude="docs, venv,.eggs,versioneer.py,build"

dist: venv
	. venv/bin/activate
	$(PYTHON) setup.py sdist bdist_wheel

dist-deploy: dist
	. venv/bin/activate
	$(PYTHON) -m twine upload --repository ${PROJECT} dist/*

dist-clean: clean
	@rm -rf venv
	@rm -rf build builds dist .eggs $(PROJECT).egg-info

version: setup.cfg venv
	. venv/bin/activate
	versioneer install

