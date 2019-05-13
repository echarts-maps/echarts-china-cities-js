const fs = require('fs');
const gulp = require('gulp');
const maker = require("echarts-mapmaker/src/maker");
const parser = require("echarts-mapmaker/src/parseGeoJson");
const mapshaper = require('mapshaper');

gulp.task('removeBorder', async () => {

  const folder = 'geojson';
  const output = 'geojson';
  const jsfolder = 'js';
  
  const data = fs.readFileSync('registry.json', 'utf8');
  const myjson = JSON.parse(data);

  for(const city of Object.keys(myjson.PINYIN_MAP)){
    if(city.indexOf("轮廓") === -1){
      let from = myjson.PINYIN_MAP[city];
      let from_filename = myjson.FILE_MAP[from];
      let to = myjson.PINYIN_MAP[city+"轮廓"];
      let to_filename = myjson.FILE_MAP[to];
      let shape_with_internal_borders = folder + '/' + from_filename + '.geojson';
      let shape_only = output + '/' + to_filename + '.geojson';
      let js = jsfolder + '/' + to_filename + '.js';
      try{
        await disolve_internal_borders(shape_with_internal_borders, shape_only, js, city);
        console.log(`${shape_with_internal_borders} -> ${shape_only}`);
      }catch(err){
        console.log(err);
        console.log(`error: ${shape_with_internal_borders} -> ${shape_only}`);
      }
    }
  }
});


async function disolve_internal_borders(geojson_file, output_file, js, map_name){
  const utf8EncodedGeoJson = JSON.parse(fs.readFileSync(geojson_file, 'utf8'));
  const geojsonFile = 'decoded.geojson';
  geojson = parser.decode(utf8EncodedGeoJson);
  fs.writeFileSync(geojsonFile, JSON.stringify(geojson));
  await disolve(geojsonFile +' -dissolve2 -o tmp.geojson');
  maker.transform('tmp.geojson', output_file, map_name);
  maker.makeJs(output_file, js, map_name+"轮廓");
}

function disolve(command){
  return new Promise((resolve, reject) => {
    mapshaper.runCommands(command, (error) => {
      if(error){reject(error);};
      resolve();
    });
  });
}
