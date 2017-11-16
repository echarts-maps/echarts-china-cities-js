# echarts-china-cities-js

[![Build Status](https://travis-ci.org/chfw/echarts-china-cities-js.svg?branch=master)](https://travis-ci.org/chfw/echarts-china-cities-js) [![npm version](https://badge.fury.io/js/echarts-china-cities-js.svg)](https://badge.fury.io/js/echarts-china-cities-js)

It collects all geo-jsons in javascript of all {{num_cities}} provincial cities
in {{num_provinces}} provinces and acts as a static asset to jupyter-echarts or your
echarts collection.

Please note, [北京](https://chfw.github.io/jupyter-echarts/echarts/beijing.js), [天津](https://chfw.github.io/jupyter-echarts/echarts/tianjin.js), [上海](https://chfw.github.io/jupyter-echarts/echarts/shanghai.js), [重庆](https://chfw.github.io/jupyter-echarts/echarts/chongqing.js), [香港](https://chfw.github.io/jupyter-echarts/echarts/xianggang.js) and [澳门](https://chfw.github.io/jupyter-echarts/echarts/aomen.js) are packaged with echarts and [jupyter-echarts](https://chfw.github.io/jupyter-echarts/preview.html) hence those 6 cities are not covered in this package.

## Installation

```
npm i echarts-china-cities-js
```

This library is included in [pyecharts](https://github.com/chenjiandongx/pyecharts) 2.2.0. No action is required from pyecharts user.

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
  	<script src="https://chfw.github.io/echarts-china-cities-js/echarts.min.js"></script>
	<script src="https://chfw.github.io/echarts-china-cities-js/dist/jiang1_xi1/nan2_chang1.min.js"></script>
  </head>
  <body>
	<div id='nan2_chang1' class='citymap'></div>
	<script src='https://chfw.github.io/echarts-china-cities-js/demo.js'></script>
	<script>
	  make_city('南昌', 'nan2_chang1');
	</script>
  </body>
</html>
```

![Usage with echarts](https://chfw.github.io/echarts-china-cities-js/nanchang.png)

## pyecharts usage

![Usage with pyecharts](https://user-images.githubusercontent.com/4280312/29755070-9bc9ae70-8b89-11e7-9bf2-bec09cb5f1a1.png)

## "first line" cities

They are not included in this package but are listed here for your reference:

[北京](https://chfw.github.io/jupyter-echarts/echarts/beijing.js), [天津](https://chfw.github.io/jupyter-echarts/echarts/tianjin.js), [上海](https://chfw.github.io/jupyter-echarts/echarts/shanghai.js), [重庆](https://chfw.github.io/jupyter-echarts/echarts/chongqing.js), [香港](https://chfw.github.io/jupyter-echarts/echarts/xianggang.js) and [澳门](https://chfw.github.io/jupyter-echarts/echarts/aomen.js)


## Featuring Cities(or for Single Download)

Cities:
{% for cprovince in registry.keys() %}
{{loop.index}}. **{{cprovince}}**:
{% for city in registry[cprovince] %}
[{{city[0]}}](https://chfw.github.io/echarts-china-cities-js/dist/{{names[cprovince]}}/{{city[1]}}.js){% if not loop.last %}, {% endif %}{% endfor %}

{% endfor %}


## Development


Please use python

```shell
$ pip install -r requirements
$ npm install
$ python makedemo.py
```

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

