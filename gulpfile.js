var gulp = require('gulp');
const fs = require('fs');
const maker = require("echarts-mapmaker/src/maker");
const parser = require("echarts-mapmaker/src/parseGeoJson");
var rename = require('gulp-rename');
var minify = require("gulp-minify");


patchTianjin = (cb) => {
  const source = "tianjin-fix/tianjin.geojson";
  const jiZhouDistrict = "tianjin-fix/jixian.geojson";
  const removed = "removed_tianjin.geojson";
  const merged = "merged_removed_tianjin.geojson";
  maker.remove(source, "蓟州区");
  maker.merge(removed, jiZhouDistrict);
  maker.makeJs(merged, '天津.js', '天津');
  gulp.src('天津.js')
    .pipe(minify({
      noSource: true,
	  ext: { min: ".js"}
	}))
	.pipe(gulp.dest('src/直辖市'));
    cb();
}

exports.default = patchTianjin
