# Code for Tokyo Data Processing Tools

---
## `tools/shp2geojson/shp2geojson.py`

shape files to geojson.

### Usage

```
$ python shp2geojson [-h] [-o OUT] files [files ...]
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

### Usage

```
$ python mlit [-h] [-o OUT] files [files ...]
```

#### positional arguments

- `files`

#### optional arguments

- `-h`, `--help`            show this help message and exit
- `-o` OUT, `--output` OUT  output file name (default: stdout)

### requirements
- Fiona==1.6.2
- Shapely==1.5.12
