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
クレジットに「国土交通省国土政策局「国土数値情報 (DATANAME)」をもとにUSERNAMEが編集・加工」を追加し
出力に埋め込む。また、属性名をコードから日本語表記に直す、行政区域コードを都道府県コードと市区町村コード
に分けた属性を追加するなどの加工も行う。


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
