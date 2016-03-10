.PHONY: clean-pyc docs

all: clean-pyc docs

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

docs:
	sphinx-apidoc -f -o docs/ cftt/
	$(MAKE) -C docs html
