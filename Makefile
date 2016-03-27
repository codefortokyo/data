.PHONY: clean-pyc docs test clean

all: clean-pyc docs test

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

docs:
	sphinx-apidoc -f -o docs/ cftt/
	$(MAKE) -C docs html

test: test_data/test_uk.zip
	find tests -name '*.py' -exec python {} \;

test_data/test_uk.zip: test_data/worldmill/docs/data/test_uk.shp
	zip test_data/test_uk.zip test_data/worldmill/docs/data/*

test_data/worldmill/docs/data/test_uk.shp: test_data
	if [ ! -e test_data/worldmill ]; then \
		git clone git@github.com:sgillies/worldmill.git test_data/worldmill;\
	fi;

test_data:
	mkdir test_data

clean:
	rm -f -r test_data
