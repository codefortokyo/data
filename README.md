# Code for Tokyo Data Processing Tools

---
## `tools/shp2geojson/shp2geojson.py`

shape files to geojson.

### usage

```
$ python shp2geojson.py [-h] [-o OUT] files [files ...]
```

#### positional arguments

- `files`

#### optional arguments

- `-h`, `--help`            show this help message and exit
- `-o` OUT, `--output` OUT  output file name (default: stdout)

### requirements
- Fiona==1.6.2
- Shapely==1.5.12

---
## `tools/shp2geojson/mlit.py`

`shp2geojson` の国土数値情報向け設定

### usage

```
$ python mlit.py [-h] [-o OUT] files [files ...]
```

#### positional arguments

- `files`

#### optional arguments

- `-h`, `--help`            show this help message and exit
- `-o` OUT, `--output` OUT  output file name (default: stdout)

### requirements
- Fiona==1.6.2
- Shapely==1.5.12

---
## `tools/geojson/filter.py`

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

## `tools/geojson/join.py`
join data with geojson.

### usage
```
$ join.py [-h] [-i I] [-d DELIM] [-o O] key dictionary
```

#### positional arguments:
  `key`                   key file name or raw string which represents join
                        keys.
  `dictionary`            dictionary file (json,csv or tsv) name

#### optional arguments:
  `-h`, `--help`            show this help message and exit
  `-i` I, `--input` I       input file name (default: stdin)
  `-d` DELIM, `--delimiter` DELIM
                        delimitor for key string
  `-o` O, `--output` O      output file name (default: stdout)
