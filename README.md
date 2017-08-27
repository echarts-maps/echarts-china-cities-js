# echarts-china-cities-js

It collects all geo-jsons in javascript of all Chinese cities and acts as a static
asset to jupyter-echarts.


# Development

Please use python

```shell
$ python makedemo.py
```

# Test

```shell
$ pip install test/requirements.txt
$ npm test
```


# License

This bundling code is MIT license. The geojson libraries are downloaded from
AMap.com(高德地图) via echarts-map-tool, hence are subjected to AMap's license. Similiar
to google's map dadta, it is free as long as the public's access to your files
are free. And you shall not start making commercial applications using the
files in this package without engaging AMap.com.