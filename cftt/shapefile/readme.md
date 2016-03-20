# `cftt.shapefile`

## `cftt.shapefile.shp2geojson`

shape files to geojson.

### usage

```sh
$ python -m cftt.shapefile.shp2geojson [-h] [-e ENCODE] [-o OUT] [-a]
                                       input [input ...]
```

#### positional arguments

- `input`
    - path to shape file or zip file, URL to zip file

#### optional arguments:

- `-h`, `--help`
    - show this help message and exit
- `-e` ENCODE, `--encode` ENCODE
    - encoding (default: utf-8)
- `-o` OUT, `--output` OUT
    - output file name (default: stdout)
- `-a`, `--aggregate`
    - aggregate the output (default: False)

---

## `cftt.shapefile.mlit`

`cftt.shapefile.shp2geojson` の国土数値情報向け設定。


### usage

```sh
$ python -m cftt.shapefile.mlit [-h] [-e ENCODE] [-o OUT] [-a] [-d DATANAME] [-u USERNAME]
                                [-p PUB]
                                input [input ...]
```

#### positional arguments

- `input`
    - path to shape file or zip file, URL to zip file

#### optional arguments:

- `-h`, `--help`
    - show this help message and exit
- `-e` ENCODE, `--encode` ENCODE
    - encoding (default: utf-8)
- `-o` OUT, `--output` OUT
    - output file name (default: stdout)
- `-a`, `--aggregate`
    - aggregate the output (default: False)
- `-d` DATANAME, `--dataname` DATANAME
    - name of data (default: empty)
- `-u` USERNAME, `--username` USERNAME
    - editor name (default: login user name)
- `-p` PUB, `--publishdate` PUB
    - publish date of this data

### requirements
- Fiona>=1.6.2
- Shapely>=1.5.12
