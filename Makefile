.PHONY: clean-pyc docs test clean

all: clean-pyc docs test

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

docs:
	sphinx-apidoc -f -o docs/ cftt/
	$(MAKE) -C docs html

test: test_data/shapefile/test_uk.zip test_data/shapefile/test_uk/test_uk.shp\
	test_data/geojson/japan.geojson test_data/geojson/japan.zip
	find tests -name '*.py' -exec python {} \;

test_data/shapefile/test_uk.zip: test_data/worldmill/docs/data/test_uk.shp
	mkdir -p test_data/shapefile
	zip test_data/shapefile/test_uk.zip test_data/worldmill/docs/data/*

test_data/worldmill/docs/data/test_uk.shp:
	mkdir -p test_data
	git clone git@github.com:sgillies/worldmill.git test_data/worldmill

test_data/shapefile/test_uk/test_uk.shp: test_data/worldmill/docs/data/test_uk.shp
	mkdir -p test_data/shapefile/test_uk
	cp test_data/worldmill/docs/data/test_uk.* test_data/shapefile/test_uk/

test_data/dataofjapan/japan.geojson:
	mkdir -p test_data
	git clone git@github.com:dataofjapan/land.git test_data/dataofjapan

test_data/geojson/japan.geojson: test_data/dataofjapan/japan.geojson
	mkdir -p test_data/geojson
	cp test_data/dataofjapan/japan.geojson test_data/geojson/japan.geojson

test_data/geojson/japan.zip: test_data/geojson/japan.geojson
	zip test_data/geojson/japan.zip test_data/geojson/japan.geojson

clean:
	rm -f -r test_data
