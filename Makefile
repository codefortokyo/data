.PHONY: clean-pyc docs test

all: clean-pyc docs test

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

docs:
	sphinx-apidoc -f -o docs/ cftt/
	$(MAKE) -C docs html

test:
	find tests -name '*.py' -exec python {} \;
