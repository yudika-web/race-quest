const{chromium}=require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'),fs=require('fs'),path=require('path');
const D=path.resolve(__dirname,'..'),URL='http://127.0.0.1:8000/visual-upgrade/blokraya-stage8-yogyakarta.html',html=()=>fs.readFileSync('/tmp/blokraya-6e/candidate.html','utf8');
async function browser(){return chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--enable-unsafe-swiftshader']})}
async function page(b,opts={}){const p=await b.newPage({viewport:{width:1280,height:800},...opts});p.setDefaultTimeout(120000);await p.route(URL,r=>r.fulfill({status:200,contentType:'text/html',body:html()}));await p.goto(URL);return p}
module.exports={D,URL,html,browser,page};
