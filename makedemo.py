# coding=utf-8
from __future__ import unicode_literals

import os
import glob
import json
import pinyin
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader
import codecs
from collections import OrderedDict

DEST_FOLDER = os.path.join('js', 'shape-with-internal-borders')
DEST_GEOJSON_FOLDER = os.path.join('geojson', 'shape-with-internal-borders')
REGISTRY_FILE = 'registry.json'

MANUAL_FIX = {
    "莆田": "pu3_tian2"
}


def list_base(src_folder):
    for folder in glob.glob(src_folder):
        if os.path.isdir(folder):
            yield folder


def list_a_directory(src_folder):
    for f in glob.glob(src_folder):
        file_name = os.path.basename(f).split('.')[0]
        if '市' in file_name:
            file_name = file_name[:-1]
        if file_name in MANUAL_FIX:
            pinyin_name = MANUAL_FIX[file_name]
        else:
            pinyin_name = pinyin.get(
                file_name, format="numerical", delimiter="_")
        yield f, file_name, pinyin_name


def minify_js(src_js, min_js):
    os.system('./node_modules/.bin/minify -o %s %s' % (min_js, src_js))


def decompress_js(min_js, geojson):
    os.system('./node_modules/.bin/decompress %s %s' % (min_js, geojson))


def minify_srcs():
    name_dict, raw_rendering_dict = {}, defaultdict(list)
    for folder in list_base('src/*'):
        cfolder = os.path.basename(folder)
        pfolder = pinyin.get(cfolder, format="numerical", delimiter="_")
        _dest_folder = DEST_FOLDER
        name_dict[cfolder] = pfolder
        if not os.path.exists(_dest_folder):
            os.mkdir(_dest_folder)
        all_files = list_a_directory(os.path.join(folder, "*.js"))
        for src_file, cname, pname in all_files:
            _dest_file = os.path.join(_dest_folder,
                                      "%s_%s.js" % (pfolder, pname))
            print("%s-> %s, %s -> %s" % (cname, pname, src_file, _dest_file))
            minify_js(src_file, _dest_file)
            raw_rendering_dict[cfolder].append((cname, pname))
    return name_dict, raw_rendering_dict


def decomporess():
    name_dict, raw_rendering_dict = {}, defaultdict(list)
    for folder in list_base('src/*'):
        cfolder = os.path.basename(folder)
        pfolder = pinyin.get(cfolder, format="numerical", delimiter="_")
        _dest_folder = DEST_GEOJSON_FOLDER
        name_dict[cfolder] = pfolder
        if not os.path.exists(_dest_folder):
            os.mkdir(_dest_folder)
        all_files = list_a_directory(os.path.join(folder, "*.js"))
        for src_file, cname, pname in all_files:
            _dest_file = os.path.join(_dest_folder,
                                      "%s_%s.geojson" % (pfolder, pname))
            print("%s-> %s, %s -> %s" % (cname, pname, src_file, _dest_file))
            decompress_js(src_file, _dest_file)
            raw_rendering_dict[cfolder].append((cname, pname))
    return name_dict, raw_rendering_dict


def write_preview(name_dict, rendering_dict, provinces,
                  cities, geojson_rendering_dict):
    jinja2_env = Environment(
        loader=FileSystemLoader('./templates'),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True)
    template = jinja2_env.get_template('index.html')
    html = template.render(names=name_dict, registry=rendering_dict,
                           js_folder="js/shape-with-internal-borders",
                           num_cities=cities)
    with codecs.open('preview.html', 'wb', 'utf-8') as f:
        f.write(html)

    template = jinja2_env.get_template('shape-only.html')
    html = template.render(names=name_dict, registry=rendering_dict,
                           js_folder="js/shape-only",
                           num_cities=cities)
    with codecs.open('shape-only-preview.html', 'wb', 'utf-8') as f:
        f.write(html)

    config = jinja2_env.get_template('config.json')
    config_json = config.render(
        names=name_dict, registry=rendering_dict,
        geojson_registry=geojson_rendering_dict)
    registry_file = REGISTRY_FILE
    with codecs.open(registry_file, 'w', 'utf-8') as f:
        f.write(config_json)

    readme = jinja2_env.get_template('README.md')
    readme_txt = readme.render(
        names=name_dict, registry=rendering_dict,
        num_provinces=provinces, num_cities=cities
    )
    with codecs.open('README.md', 'wb', 'utf-8') as f:
        f.write(readme_txt)


def doall():
    name_dict, raw_rendering_dict = minify_srcs()
    geojson_dict, geojson_rendering_dict = decomporess()

    # adding direct cities
    cnames = ['北京', '澳门', '重庆', '上海', '天津', '香港']
    cities = ['beijing', 'aomen', 'chongqing', 'shanghai',
              'tianjin', 'xianggang']
    for cname, pname in zip(cnames, cities):
        src_file = os.path.join('node_modules',
                                'echarts',
                                'map',
                                'js',
                                'province',
                                '%s.js' % pname)
        _dest_file = os.path.join(DEST_FOLDER, '%s.js' % pname)
        minify_js(src_file, _dest_file)
        print("%s-> %s, %s -> %s" % (cname, pname, src_file, _dest_file))
        raw_rendering_dict['直辖市'].append((cname, pname))
        _geojson_file = os.path.join(DEST_GEOJSON_FOLDER, '%s.geojson' % pname)
        decompress_js(src_file, _geojson_file)
        print("%s-> %s, %s -> %s" % (cname, pname, src_file, _geojson_file))
        geojson_rendering_dict['直辖市'].append((cname, pname))
    # statistics
    count = 0
    rendering_dict = OrderedDict()
    sorted_provinces = sorted(raw_rendering_dict.keys(),
                              key=lambda x: pinyin.get(x, format='numerical'))
    for cprovince in sorted_provinces:
        count += len(raw_rendering_dict[cprovince])
        rendering_dict[cprovince] = sorted(
            raw_rendering_dict[cprovince], key=lambda x: x[1])
    provinces, cities = len(rendering_dict.keys()), count

    write_preview(name_dict, rendering_dict, provinces, cities, geojson_rendering_dict)

    # custom data structure
    external = defaultdict(list)
    for key, value in raw_rendering_dict.items():
        if key != '直辖市':
            for city in value:
                external[key].append(city[0])
    with codecs.open('structure.json', 'wb', 'utf-8') as f:
        json.dump(external, f)


if __name__ == '__main__':
    doall()
