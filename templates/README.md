# echarts-china-cities-js

It collects all geo-jsons in javascript of all {{num_cities}} provincial cities
in {{num_provinces}} and acts as a static asset to jupyter-echarts or your
echarts collection.

<<<<<<< HEAD
# Feature

Cities:
{% for cprovince in registry.keys() %}
**{{cprovince}}**:
{% for city in registry[cprovince] %}
{{city[0]}}{% if not loop.last %}, {% endif %}{% endfor %}
=======
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
  	<script src="https://chfw.github.io/echarts-china-cities-js/echarts.min.js"></script>
	<script src="https://chfw.github.io/echarts-china-cities-js/dist/jiang1_xi1/nan2_chang1.js"></script>
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

This library is included in pyecharts 2.0.2. No action is required from you.

![Usage with pyecharts](https://user-images.githubusercontent.com/4280312/29755070-9bc9ae70-8b89-11e7-9bf2-bec09cb5f1a1.png)

## Featuring Cities(or for Single Download)

Cities:
{% for cprovince in registry.keys() %}
{{loop.index}}. **{{cprovince}}**:
{% for city in registry[cprovince] %}
[{{city[0]}}]("https://chfw.github.io/echarts-china-cities-js/dist/{{names[cprovince]}}/{{city[1]}}.js"){% if not loop.last %}, {% endif %}{% endfor %}
>>>>>>> master

{% endfor %}


<<<<<<< HEAD
# Development
=======
## Development
>>>>>>> master

Please use python

```shell
$ python makedemo.py
```

<<<<<<< HEAD
# Test
=======
## Test
>>>>>>> master

```shell
$ pip install test/requirements.txt
$ npm test
```

<<<<<<< HEAD
# License

This bundling code is MIT license. The geojson libraries are downloaded from
AMap.com(高德地图) via echarts-map-tool, hence are subjected to AMap's license. Similiar
to google's map dadta, it is free as long as the public's access to your files
are free. And you shall not start making commercial applications using the
files in this package without engaging AMap.com.
=======
## License

The geojson files are downloaded from AMap.com(高德地图) via [echarts-map-tool](http://ecomfe.github.io/echarts-map-tool/),
hence are subjected to AMap's [service and content license](https://lbs.amap.com/home/terms/).

**No content right** have been transferred to you and you shall **engage AMap.com** before
making commercial applications using the files in this package. No liability/Guarantee were
given for any error or flaws in the downloaded files.

### Free usage instructions

Similiar to google's map data, it is free as long as the public's access to your files
are free. 

This bundling code(makedemo.py) is MIT license.
>>>>>>> master
