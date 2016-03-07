# -*- coding: utf-8 -*-

import shp2geojson;

m = {"N03_001":"都道府県名","N03_002":"支庁・振興局名","N03_003":"郡・政令都市名","N03_004":"市区町村名","N03_007":"行政区域コード"};

shpAggr = shp2geojson.shapeAggregator().prop(lambda s,p:{m[k]:p[0][k] if k in p[0] else None for k in m});

if __name__ == '__main__':
  shp2geojson.mainFunc(shpAggr);
