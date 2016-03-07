## `filter.py`

filter geojson by property.

### usage
```
$ python filter.py [-h] [-i I] [-o O] filters [filters ...]
```


#### positional arguments:
- `filters`           filter file name or python dictionary object

#### optional arguments:
-  `-h`, `--help`        show this help message and exit
-  `-i` I, `--input` I   input file name (default: stdin)
-  `-o` O, `--output` O  output file name (default: stdout)

## `join.py`
join data with geojson.

### usage
```
$ join.py [-h] [-i I] [-d DELIM] [-o O] key dictionary
```

#### positional arguments:
-  `key`                   key file name or raw string which represents join
                        keys.
-  `dictionary`            dictionary file (json,csv or tsv) name

#### optional arguments:
-  `-h`, `--help`            show this help message and exit
-  `-i` I, `--input` I       input file name (default: stdin)
-  `-d` DELIM, `--delimiter` DELIM
                        delimitor for key string
-  `-o` O, `--output` O      output file name (default: stdout)

## `prop2csv.py`

extract properties from the input geojson and dump into csv.

#### usage
```
$ prop2csv.py [-h] [-i I] [-d D] [-o O]
```

#### optional arguments:
-  `-h`, `--help`           show this help message and exit
-  `-i` I, `--input` I      input file name (default: stdin)
-  `-d` D, `--delimiter` D  delimiter (default: ,)
-  `-o` O, `--output` O     output file name (default: stdout)
