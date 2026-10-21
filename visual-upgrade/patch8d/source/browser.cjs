const{chromium}=require(process.env.PLAYWRIGHT_MODULE||'/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'),fs=require('fs'),path=require('path');
const D=path.resolve(__dirname,'..'),URL='http://127.0.0.1:8000/visual-upgrade/blokraya-patch8d-controls.html',html=()=>fs.readFileSync(process.env.BLOKRAYA_RELEASE==='1'?path.resolve(D,'../blokraya-patch8d-controls.html'):path.resolve(D,'../blokraya-patch8d-controls.html'),'utf8');
async function browser(){return chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--enable-unsafe-swiftshader']})}
async function page(b,opts={}){const p=await b.newPage({viewport:{width:1280,height:800},...opts});p.setDefaultTimeout(120000);await p.route(URL,r=>r.fulfill({status:200,contentType:'text/html',body:html()}));await p.goto(URL);return p}
module.exports={D,URL,html,browser,page};
