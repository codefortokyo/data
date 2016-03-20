# `cftt.shapefile`

## `cftt.shapefile.shp2geojson`

shape files to geojson.

### usage

```sh
$ python -m cftt.shapefile.shp2geojson [-h] [-e ENCODE] [-o OUT] [-a] input [input ...]
```

#### positional arguments

  `input`

#### optional arguments:

  -h, --help            show this help message and exit
  -e ENCODE, --encode ENCODE
                        encoding (default: utf-8)
  -o OUT, --output OUT  output file name (default: stdout)
  -a, --aggregate       aggregate the output (default: False)


## `cftt.shapefile.mlit`

`cftt.shapefile.shp2geojson` の国土数値情報向け設定。


### usage

```sh
$ python -m cftt.shapefile.mlit [-h] [-d DATANAME] [-e ENCODE] [-u USERNAME] [-a] [-o OUT]
               input [input ...]
```

#### positional arguments:

  `input`

#### optional arguments:
  - `-h`, `--help`:            show this help message and exit
  - `-d` DATANAME, `--dataname` DATANAME:
                        name of data (default: empty)
  - `-e` ENCODE, `--encode` ENCODE:
                        encoding (default: utf-8)
  - `-u` USERNAME, `--username` USERNAME:
                        editor name (default: login user name)
  - `-a`, `--aggregate`:       aggregate the output (default: False)
  - `-o` OUT, `--output` OUT:  output file name (default: stdout)

### requirements
- Fiona>=1.6.2
- Shapely>=1.5.12
