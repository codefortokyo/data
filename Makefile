.PHONY: clean-pyc docs test clean

all: clean-pyc docs test

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

docs:
	sphinx-apidoc -f -o docs/ cftt/
	$(MAKE) -C docs html

test: test_data/test_uk.zip test_data/shapefile/test_uk.shp
	find tests -name '*.py' -exec python {} \;

test_data/test_uk.zip: test_data/worldmill/docs/data/test_uk.shp
	zip test_data/test_uk.zip test_data/worldmill/docs/data/*

test_data/worldmill/docs/data/test_uk.shp:
	mkdir -p test_data
	git clone git@github.com:sgillies/worldmill.git test_data/worldmill

test_data/shapefile/test_uk.shp: test_data/worldmill/docs/data/test_uk.shp
	mkdir -p test_data/shapefile
	cp test_data/worldmill/docs/data/test_uk.* test_data/shapefile/

clean:
	rm -f -r test_data
