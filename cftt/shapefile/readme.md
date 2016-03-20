
## `shp2geojson.py`

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
## `mlit.py`
`python -m cftt.shapefile.mlit http://nlftp.mlit.go.jp/ksj/gml/data/N03/N03-15/N03-150101_13_GML.zip > out.json`
`` の国土数値情報向け設定

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
