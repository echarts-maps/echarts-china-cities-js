const fs = require('fs');
const gulp = require('gulp');
const maker = require("echarts-mapmaker/src/maker");
const parser = require("echarts-mapmaker/src/parseGeoJson");
const mapshaper = require('mapshaper');

gulp.task('removeBorder', async () => {

  const folder = 'geojson/shape-with-internal-borders';
  const output = 'geojson/shape-only';
  const jsfolder = 'js/shape-only';
  
  const data = fs.readFileSync('registry.json', 'utf8');
  const myjson = JSON.parse(data);

  for(const city of Object.keys(myjson.PINYIN_MAP)){
    let pinying = myjson.PINYIN_MAP[city];
    let filename = myjson.FILE_MAP[pinying];
    let geojson = folder + '/' + filename + '.geojson';
    let dest = output + '/' + filename + '.geojson';
    let js = jsfolder + '/' + filename + '.js';
    try{
      await disolve_internal_borders(geojson, dest, js, city);
      console.log(`${geojson} -> ${dest}`);
    }catch(err){
      console.log(err);
      console.log(`error: ${geojson} -> ${dest}`);    
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
  maker.makeJs(output_file, js, map_name);
}

function disolve(command){
  return new Promise((resolve, reject) => {
    mapshaper.runCommands(command, (error) => {
      if(error){reject(error);};
      resolve();
    });
  });
}
