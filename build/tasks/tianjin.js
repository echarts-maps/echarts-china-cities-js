const fs = require('fs');
const gulp = require('gulp');
const maker = require("echarts-mapmaker/src/maker");
const parser = require("echarts-mapmaker/src/parseGeoJson");
var rename = require('gulp-rename');
var minify = require("gulp-minify");


gulp.task('patchTianjin', () => {
  const source = "tianjin-fix/tianjin.geojson";
  const jiZhouDistrict = "tianjin-fix/jixian.geojson";
  const removed = "removed_tianjin.geojson";
  const merged = "merged_removed_tianjin.geojson";
  maker.remove(source, "蓟州区");
  maker.merge(removed, jiZhouDistrict);
  maker.makeJs(merged, 'tianjin.js', '天津');
  gulp.src(merged, {base: '.'})
    .pipe(rename('tianjin.geojson'))
    .pipe(gulp.dest('geojson/shape-with-internal-borders'));
  gulp.src('tianjin.js')
    .pipe(minify({
      noSource: true,
	  ext: { min: ".js"}
	}))
	.pipe(gulp.dest('js/shape-with-internal-borders'));
})
