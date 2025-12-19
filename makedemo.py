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
import shutil

DEST_FOLDER = os.path.join("js", "shape-with-internal-borders")
DEST_GEOJSON_FOLDER = os.path.join("geojson", "shape-with-internal-borders")
REGISTRY_FILE = "registry.json"

MANUAL_FIX = {"莆田": "pu3_tian2"}
CONTOUR = "轮廓"


def list_base(src_folder):
    for folder in glob.glob(src_folder):
        if os.path.isdir(folder):
            yield folder


def list_a_directory(src_folder):
    for f in glob.glob(src_folder):
        file_name = os.path.basename(f).split(".")[0]
        if "市" in file_name:
            file_name = file_name[:-1]
        if file_name in MANUAL_FIX:
            pinyin_name = MANUAL_FIX[file_name]
        else:
            pinyin_name = pinyin.get(file_name, format="numerical", delimiter="_")
        yield f, file_name, pinyin_name


def make_js(geojson, js, chinese_name):
    command = "./node_modules/.bin/makejs %s %s %s" % (geojson, js, chinese_name)
    print(command)
    os.system(command)


def minify_js(src_js, min_js):
    os.system("./node_modules/.bin/minify -o %s %s" % (min_js, src_js))


def decompress_js(min_js, geojson):
    os.system("./node_modules/.bin/decompress %s %s" % (min_js, geojson))


def remove_internal_borders():
    with open(REGISTRY_FILE, "r") as f:
        registry = json.load(f)
        folder = output = "geojson"
        jsfolder = "js"
        pinyin_map = registry["PINYIN_MAP"]
        contour = CONTOUR
        for city in pinyin_map:
            if contour in city:
                continue
            print(f"Processing {city}")
            fm = pinyin_map[city]
            fm_filename = registry["FILE_MAP"][fm]
            to = pinyin_map[city + contour]
            to_filename = registry["FILE_MAP"][to]
            shape_with_internal_borders = f"{folder}/{fm_filename}.geojson"
            shape_only = f"{output}/{to_filename}.geojson"
            js = f"{jsfolder}/{to_filename}.js"

            try:
                disolve_internal_borders(
                    shape_with_internal_borders, shape_only, js, city
                )
                print(f"{shape_with_internal_borders} -> {shape_only}")
            except Exception as e:
                print(e)
                print(f"error : {shape_with_internal_borders} -> {shape_only}")


def disolve_internal_borders(shape, shape_only, js, city):
    os.system(f"./node_modules/.bin/mapshaper {shape}  -dissolve2 -o tmp.geojson")
    with open("tmp.geojson", "r") as f:
        shaper = json.load(f)

    echarts_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": city},
                "geometry": shaper["geometries"][0],
            }
        ],
    }
    with open(shape_only, "w") as f2:
        json.dump(echarts_geojson, f2)

    make_js(shape_only, js, city + CONTOUR)


def minify_srcs():
    name_dict, raw_rendering_dict = {}, defaultdict(list)
    for folder in list_base("src/*"):
        cfolder = os.path.basename(folder)
        pfolder = pinyin.get(cfolder, format="numerical", delimiter="_")
        _dest_folder = DEST_FOLDER
        name_dict[cfolder] = pfolder
        if not os.path.exists(_dest_folder):
            os.mkdir(_dest_folder)
        all_files = list_a_directory(os.path.join(folder, "*.js"))
        for src_file, cname, pname in all_files:
            _dest_file = os.path.join(_dest_folder, "%s_%s.js" % (pfolder, pname))
            print("%s-> %s, %s -> %s" % (cname, pname, src_file, _dest_file))
            minify_js(src_file, _dest_file)
            raw_rendering_dict[cfolder].append((cname, pname))
    return name_dict, raw_rendering_dict


def minify_geojson():
    name_dict, raw_rendering_dict = {}, defaultdict(list)
    for folder in list_base("src/*"):
        cfolder = os.path.basename(folder)
        pfolder = pinyin.get(cfolder, format="numerical", delimiter="_")
        _dest_folder = DEST_FOLDER
        name_dict[cfolder] = pfolder
        if not os.path.exists(_dest_folder):
            os.mkdir(_dest_folder)
        all_files = list_a_directory(os.path.join(folder, "*.geojson"))
        for src_file, cname, pname in all_files:
            _dest_file = os.path.join(_dest_folder, "%s_%s.js" % (pfolder, pname))
            print("%s-> %s, %s -> %s" % (cname, pname, src_file, _dest_file))
            make_js(src_file, "tw_tmp.js", cname)
            minify_js("tw_tmp.js", _dest_file)
            raw_rendering_dict[cfolder].append((cname, pname))
    return name_dict, raw_rendering_dict


def decomporess():
    name_dict, raw_rendering_dict = {}, defaultdict(list)
    for folder in list_base("src/*"):
        cfolder = os.path.basename(folder)
        pfolder = pinyin.get(cfolder, format="numerical", delimiter="_")
        _dest_folder = DEST_GEOJSON_FOLDER
        name_dict[cfolder] = pfolder
        if not os.path.exists(_dest_folder):
            os.mkdir(_dest_folder)
        all_files = list_a_directory(os.path.join(folder, "*.js"))
        for src_file, cname, pname in all_files:
            _dest_file = os.path.join(_dest_folder, "%s_%s.geojson" % (pfolder, pname))
            print("%s-> %s, %s -> %s" % (cname, pname, src_file, _dest_file))
            decompress_js(src_file, _dest_file)
            raw_rendering_dict[cfolder].append((cname, pname))
    return name_dict, raw_rendering_dict


def decomporess_geojson():
    name_dict, raw_rendering_dict = {}, defaultdict(list)
    for folder in list_base("src/*"):
        cfolder = os.path.basename(folder)
        pfolder = pinyin.get(cfolder, format="numerical", delimiter="_")
        _dest_folder = DEST_GEOJSON_FOLDER
        name_dict[cfolder] = pfolder
        if not os.path.exists(_dest_folder):
            os.mkdir(_dest_folder)
        all_files = list_a_directory(os.path.join(folder, "*.geojson"))
        for src_file, cname, pname in all_files:
            _dest_file = os.path.join(_dest_folder, "%s_%s.geojson" % (pfolder, pname))
            print("copy: %s-> %s, %s -> %s" % (cname, pname, src_file, _dest_file))
            shutil.copy(src_file, _dest_file)
            raw_rendering_dict[cfolder].append((cname, pname))
    return name_dict, raw_rendering_dict


def write_preview(name_dict, rendering_dict, provinces, cities, geojson_rendering_dict):
    jinja2_env = Environment(
        loader=FileSystemLoader("./templates"),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = jinja2_env.get_template("index.html")
    html = template.render(
        names=name_dict,
        registry=rendering_dict,
        js_folder="js/shape-with-internal-borders",
        num_cities=cities,
    )
    with codecs.open("preview.html", "wb", "utf-8") as f:
        f.write(html)

    template = jinja2_env.get_template("shape-only.html")
    html = template.render(
        names=name_dict,
        registry=rendering_dict,
        js_folder="js/shape-only",
        num_cities=cities,
    )
    with codecs.open("shape-only-preview.html", "wb", "utf-8") as f:
        f.write(html)

    config = jinja2_env.get_template("config.json")
    config_json = config.render(
        names=name_dict,
        registry=rendering_dict,
        geojson_registry=geojson_rendering_dict,
    )
    registry_file = REGISTRY_FILE
    with codecs.open(registry_file, "w", "utf-8") as f:
        f.write(config_json)

    readme = jinja2_env.get_template("README.md")
    readme_txt = readme.render(
        names=name_dict,
        registry=rendering_dict,
        num_provinces=provinces,
        num_cities=cities,
    )
    with codecs.open("README.md", "wb", "utf-8") as f:
        f.write(readme_txt)


def doall():
    name_dict2, raw_rendering_dict2 = minify_geojson()
    return
    name_dict, raw_rendering_dict = minify_srcs()

    name_dict.update(name_dict2)
    raw_rendering_dict.update(raw_rendering_dict2)

    geojson_dict, geojson_rendering_dict = decomporess()
    geojson_dict2, geojson_rendering_dict2 = decomporess_geojson()

    geojson_dict.update(geojson_dict2)
    geojson_rendering_dict.update(geojson_rendering_dict2)

    # adding direct cities
    cnames = ["北京", "澳门", "重庆", "上海", "天津", "香港"]
    cities = ["beijing", "aomen", "chongqing", "shanghai", "tianjin", "xianggang"]
    compressed_cities = [
        "重庆",
        "上海",
    ]
    for cname, pname in zip(cnames, cities):
        src_file = os.path.join(
            "node_modules", "echarts", "map", "js", "province", "%s.js" % pname
        )
        _dest_file = os.path.join(DEST_FOLDER, "%s.js" % pname)
        raw_rendering_dict["直辖市"].append((cname, pname))
        geojson_rendering_dict["直辖市"].append((cname, pname))
        if cname in compressed_cities:
            shutil.copy(src_file, _dest_file)
            print("copy: %s-> %s, %s -> %s" % (cname, pname, src_file, _dest_file))
            geojson_src = os.path.join(
                "node_modules", "echarts", "map", "json", "province", "%s.json" % pname
            )

            _geojson_file = os.path.join(DEST_GEOJSON_FOLDER, "%s.geojson" % pname)
            shutil.copy(geojson_src, _geojson_file)
            print(
                "copy: %s-> %s, %s -> %s" % (cname, pname, geojson_src, _geojson_file)
            )
        else:
            minify_js(src_file, _dest_file)
            print("%s-> %s, %s -> %s" % (cname, pname, src_file, _dest_file))
            _geojson_file = os.path.join(DEST_GEOJSON_FOLDER, "%s.geojson" % pname)
            decompress_js(src_file, _geojson_file)
            print("%s-> %s, %s -> %s" % (cname, pname, src_file, _geojson_file))
    # statistics
    count = 0
    rendering_dict = OrderedDict()
    sorted_provinces = sorted(
        raw_rendering_dict.keys(), key=lambda x: pinyin.get(x, format="numerical")
    )
    for cprovince in sorted_provinces:
        count += len(raw_rendering_dict[cprovince])
        rendering_dict[cprovince] = sorted(
            raw_rendering_dict[cprovince], key=lambda x: x[1]
        )
    provinces, cities = len(rendering_dict.keys()), count

    write_preview(name_dict, rendering_dict, provinces, cities, geojson_rendering_dict)

    remove_internal_borders()

    # custom data structure
    external = defaultdict(list)
    for key, value in raw_rendering_dict.items():
        if key != "直辖市":
            for city in value:
                external[key].append(city[0])
    with codecs.open("structure.json", "wb", "utf-8") as f:
        json.dump(external, f)


if __name__ == "__main__":
    doall()
    remove_internal_borders()
