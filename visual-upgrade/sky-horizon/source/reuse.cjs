// Execute accepted regression suites against this distribution without copying the engine.
const fs=require('fs'),path=require('path'),Module=require('module');
exports.run=function(name,transform=s=>s){const file=path.join(__dirname,name),m=new Module(file,module);m.filename=file;m.paths=module.paths;let s=fs.readFileSync(path.join(__dirname,'../../patch4-5-responsive-hud/source',name),'utf8');s=s.replaceAll('race-quest-pro-patch4-5.html','race-quest-pro-sky-horizon.html').replaceAll('/patch4-5-responsive-hud/','/sky-horizon/');m._compile(transform(s),file);return m.exports};
