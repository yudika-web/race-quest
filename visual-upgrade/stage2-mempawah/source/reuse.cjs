// Reuse accepted regression suites; redirect outputs without editing historical tests.
const fs=require('fs'),path=require('path'),Module=require('module');
exports.run=function(name,transform){const file=path.join(__dirname,name),m=new Module(file,module);m.filename=file;m.paths=module.paths;let s=fs.readFileSync(path.join(__dirname,'../../batch1/source',name),'utf8');s=s.replaceAll('race-quest-pro-batch1.html','race-quest-pro-mempawah-stage2.html').replaceAll('/batch1/','/stage2-mempawah/');s=transform?transform(s):s;m._compile(s,file);return m.exports};
