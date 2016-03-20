## `cftt.shapefile.mlit`

`cftt.shapefile.shp2geojson` の国土数値情報向け設定。


### usage

```sh
$ python -m cftt.shapefile.mlit [-h] [-d DATANAME] [-e ENCODE] [-u USERNAME] [-a] [-o OUT]
               input [input ...]
```

#### positional arguments:
  input

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

### example

```sh
$ python -m cftt.shapefile.mlit http://path.to.mlit/some_shapefile.zip -o output.json
```

### requirements
- Fiona>=1.6.2
- Shapely>=1.5.12
