# echarts-china-cities-js

[![Build Status](https://travis-ci.org/echarts-maps/echarts-china-cities-js.svg?branch=master)](https://travis-ci.org/echarts-maps/echarts-china-cities-js) [![npm version](https://badge.fury.io/js/echarts-china-cities-js.svg)](https://badge.fury.io/js/echarts-china-cities-js)

It collects all geo-jsons in javascript of all {{num_cities}} provincial cities
in {{num_provinces}} provinces and acts as a static asset to jupyter-echarts or your
echarts collection.

!!! note

   This repo is not associated with Apache ECharts (incubating) project

## Feature highlights

1. City shape with and without internal borders
1. City shape in js and json formats.


## Installation

```
npm i echarts-china-cities-js
```

## echarts usage


```
<html>
  <head>
    <meta charset="utf-8" />
	<style>
	  .citymap{
	  width: 100%;
	  height: 100%;
	  }
	</style>
  	<script src="https://echarts-maps.github.io/echarts-china-cities-js/echarts.min.js"></script>
	<script src="https://echarts-maps.github.io/echarts-china-cities-js/js/shape-with-internal-borders/jiang1_xi1_nan2_chang1.js"></script>
  </head>
  <body>
	<div id='nan2_chang1' class='citymap'></div>
	<script src='https://echarts-maps.github.io/echarts-china-cities-js/demo.js'></script>
	<script>
	  make_city('南昌', 'nan2_chang1');
	</script>
  </body>
</html>
```

![Usage with echarts](https://echarts-maps.github.io/echarts-china-cities-js/nanchang.png)

## pyecharts usage

![Usage with pyecharts](https://user-images.githubusercontent.com/4280312/29755070-9bc9ae70-8b89-11e7-9bf2-bec09cb5f1a1.png)


## Featuring Cities(or for Single Download)

Cities:
{% for cprovince in registry.keys() %}
{{loop.index}}. **{{cprovince}}**:
{% for city in registry[cprovince] %}
[{{city[0]}}](https://echarts-maps.github.io/echarts-china-cities-js/echarts-china-cities-js/{{names[cprovince]}}_{{city[1]}}.js){% if not loop.last %}, {% endif %}{% endfor %}

{% endfor %}


## Development


Please use python

```shell
$ pip install -r requirements
$ npm install
$ python makedemo.py
$ gulp
```

## data flow

1. makedemo: src -> geojson and js folder with shapes
2. gulp: geojson -> shape-only js and geojson

## Test

```shell
$ pip install test/requirements.txt
$ npm test
```

## License

The geojson files are downloaded from AMap.com(高德地图) via [echarts-map-tool](http://ecomfe.github.io/echarts-map-tool/),
hence are subjected to AMap's [service and content license](https://lbs.amap.com/home/terms/).

**No content right** have been transferred to you and you shall **engage AMap.com** before
making commercial applications using the files in this package. No Liability nor Guarantee were
given for any error or flaws in the downloaded files.

### Free usage instructions

Similiar to google's map data, it is free as long as the public's access to your files
are free. 

This bundling code(makedemo.py) is MIT license.

